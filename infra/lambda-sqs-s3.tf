resource "aws_lambda_function" "sqs_to_s3" {
  filename      = "lambdas/lambda-sqs-s3/function.zip"
  function_name = "sqs_to_s3"
  role          = aws_iam_role.s3_and_sqs_access.arn
  handler       = "lambda.lambda_handler"
  layers = [
    "arn:aws:lambda:us-east-2:770693421928:layer:Klayers-python38-pandas:39",
    "arn:aws:lambda:us-east-2:770693421928:layer:Klayers-python38-numpy:20",
    aws_lambda_layer_version.sqs_s3.arn,
    ]
  memory_size = 256
  runtime = "python3.8"
}
