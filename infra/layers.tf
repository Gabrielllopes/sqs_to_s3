resource "aws_lambda_layer_version" "sqs_s3" {
  filename   = "custom_layers/sqs_s3/sqs_to_s3_layer.zip"
  layer_name = "sqs_s3"

  compatible_runtimes = ["python3.8"]
}
