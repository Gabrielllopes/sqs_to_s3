# SQS to S3

<img src=/img/arc.png>

This project propose an architecture for saving sqs messages into S3 in a JSON format. 
It does that using AWS Lambda and all the components are initiated with terraform.

## How to recreate

1. Create the lambda zip for deploy and custom layer.
```bash
$ cd infra/custom_layers/sqs_s3/
$ bash layer_create.sh
$ cd ../../lambdas/
$ bash zip_lambdas.sh
```
2. Initiate the terrafrom
```bash
$ cd ../
$ terraform init
$ terraform apply
```

## Using the lambda to save the sqs
All the paramters are passed to the function as payload in JSON format
### Paramters
* sqs_name = Name of the sqs queue
* db = sufix for saving into s3
* table = sufix for saving into s3
* s3_bucket_and_folder = bucket where the data will be saved
* partition = sufix for saving into s3

Final format on S3:
```{s3_bucket_and_folder}/{db}/{table}/{partition}/file.json```

```bash
aws lambda invoke \
--cli-binary-format raw-in-base64-out \
--function-name sqs_to_s3 \
--invocation-type RequestResponse \
--payload '{ "sqs_name":"poc-lambdas3", "db":"database-test", "table":"tabela_imaginaria", "s3_bucket_and_folder":"s3://test-glue-create-table-terraform-8888/teste_dirr/", "partition":"20-09-2021" }' \
response.json
```
## infra
Terraform code of the aws components.

## infra/lambdas
Code of the lambda functions.

## infra/custom_layers
Code of the custom layers.
## Terraform limitation
Terraform has the limitation of not updating layers or lambda functions if
 no terraform code has change (e.g: you update your lambda code, but there is 
 no TF update) in this case the terraform apply will not see this trigger.

This is an oppen issue and there is two workarounds:
1. Do a terraform destroy and then a terraform apply
2. Create a aws cli just to update the lambda and layer

## Layers
[Public layers](https://github.com/keithrozario/Klayers/tree/master/deployments/python3.8/arns)  
[Build a custom layer](https://stackoverflow.com/questions/46185297/using-numpy-in-aws-lambda)