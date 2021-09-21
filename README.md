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