resource "aws_lambda_layer_version" "pandas" {
  filename   = "custom_layers/pandas/pandas_layer.zip"
  layer_name = "pandas"

  compatible_runtimes = ["python3.8"]
}

resource "aws_lambda_layer_version" "numpy" {
  filename   = "custom_layers/numpy/numpy_layer.zip"
  layer_name = "numpy"

  compatible_runtimes = ["python3.8"]
}