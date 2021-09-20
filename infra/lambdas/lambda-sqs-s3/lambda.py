import boto3
import json
import logging
import pandas as pd
import uuid

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sqs_client = boto3.client("sqs")
glue_client = boto3.client("glue")

SQS_NAME = "poc-lambdas3"
DB = "db1"
TABLE = "tabelateste"
SAVEPATH_S3 = "s3://test-glue-create-table-terraform-8888/folder-test/"
SUBDIV = "17-09-2021"


def lambda_handler(event, context):
    logger.info("====> SQS TO S3 LAMBDA INIT")
    # Because lambda has a memory limitation
    # we will limit the amout of messages processed at the same time

    # list the amout of messages
    try:
        sqs_response = sqs_client.get_queue_attributes(
            QueueUrl=SQS_NAME, AttributeNames=["ApproximateNumberOfMessages"]
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
                sqs_to_s3(sqs_name=SQS_NAME, total=300)
                total_messages -= 300
            else:
                sqs_to_s3(sqs_name=SQS_NAME, total=total_messages)
                total_messages = 0
        except Exception as e:
            logger.error("Error while reading sqs.\n{}".format(e))
            raise


def sqs_to_s3(sqs_name, total):
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
        df.to_parquet(
            f"{SAVEPATH_S3}{DB}/{TABLE}/{SUBDIV}/",
            compression="gzip"
        )
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
