resource "aws_lambda_function" "sqs_to_s3" {
  filename      = "lambdas/lambda-sqs-s3/function.zip"
  function_name = "sqs_to_s3"
  role          = aws_iam_role.s3_and_sqs_access.arn
  handler       = "lambdas/lambda-sqs-s3/lambda.lambda_handler"
  layers = [
    aws_lambda_layer_version.pandas.arn,
    aws_lambda_layer_version.numpy.arn
    ]

  runtime = "python3.8"
}
