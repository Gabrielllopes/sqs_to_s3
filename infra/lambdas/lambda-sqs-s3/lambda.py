import boto3
import json
import logging
import pandas as pd
import uuid
import s3fs
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sqs_client = boto3.client("sqs")
glue_client = boto3.client("glue")
# Example usage
"""
aws lambda invoke \
--function-name sqs_to_s3 \
--invocation-type RequestResponse \
--payload '{ "sqs_name":"poc-lambdas3", "db":"database-test", "table":"tabela_imaginaria", "s3_bucket_and_folder":"s3://test-glue-create-table-terraform-8888/teste_dirr/", "partition":"20-09-2021" }' \
response.json
"""

def lambda_handler(event, context):

    sqs_name = event["sqs_name"]
    db = event["db"]
    table = event["table"]
    s3_bucket = event["s3_bucket_and_folder"]
    partition = event["partition"]

    logger.info("====> SQS TO S3 LAMBDA INIT")
    # Because lambda has a memory limitation
    # we will limit the amout of messages processed at the same time

    # list the amout of messages
    try:
        sqs_response = sqs_client.get_queue_attributes(
            QueueUrl=sqs_name, AttributeNames=["ApproximateNumberOfMessages"]
        )
        total_messages = \
            int(sqs_response["Attributes"]["ApproximateNumberOfMessages"])

    except Exception as e:
        logger.error("Error while reading sqs.\n{}".format(e))
        raise

    while total_messages > 0:
        try:
            # 1 message aprox 256 kb
            # 300 messages aprox 75mb
            # OBS: lambda functing default memory is 128mb
            if total_messages > 300:
                sqs_to_s3(
                    sqs_name=sqs_name,
                    total=300,
                    database=db,
                    table=table,
                    s3_bucket=s3_bucket,
                    partition=partition)
                total_messages -= 300
            else:
                sqs_to_s3(
                    sqs_name=sqs_name,
                    total=total_messages,
                    database=db,
                    table=table,
                    s3_bucket=s3_bucket,
                    partition=partition)
                total_messages = 0
        except Exception as e:
            logger.error("Error while reading sqs.\n{}".format(e))
            raise


def sqs_to_s3(sqs_name, total, database, table, s3_bucket, partition):
    logger.info("====> FUNCTION sqs_to_s3")
    chunk = []
    messages_id = []
    try:
        # Reciving messages
        for _ in range(0, total):
            response = sqs_client.receive_message(QueueUrl=sqs_name)
            chunk.append(json.loads(response["Messages"][0]["Body"]))
            messages_id.append(
                {
                    "Id": str(uuid.uuid4())[:8],
                    "ReceiptHandle": response["Messages"][0]["ReceiptHandle"],
                }
            )
    except Exception as e:
        logger.error("Error while reading sqs message.\n{}".format(e))
        raise
    try:
        # Converting to pandas dataframe
        df = pd.json_normalize(chunk)

    except Exception as e:
        logger.error(
            "Error converting message to dataframe."
            "\nError:{}"
            "\nMessage:{}".format(e, chunk)
        )
        raise

    try:
        # saving into parquet
        filename=str(time.time())[-10:-1]+".json"
        df.to_json(f"{s3_bucket}{database}/{table}/{partition}/{filename}")
    except Exception as e:
        logger.error("Error saving dataframe into s3.\nError:{}".format(e))
        raise

    try:
        # Deleting message from sqs
        sqs_client.delete_message_batch(QueueUrl=sqs_name, Entries=messages_id)
    except Exception as e:
        logger.error("Error while deleting sqs message.\nError:{}".format(e))
        raise

    logger.info("====> SUCCESS EXIT sqs_to_s3")
