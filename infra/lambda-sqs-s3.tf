resource "aws_lambda_function" "sqs_to_s3" {
  filename      = "lambdas/lambda-sqs-s3/function.zip"
  function_name = "sqs_to_s3"
  role          = aws_iam_role.s3_and_sqs_access.arn
  handler       = "lambda.lambda_handler"

  runtime = "python3.8"
}