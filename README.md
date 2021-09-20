# bi-data-lake

## infra
Terraform code of the aws components

## lambda code
Code of the lambda functions

## Terraform limitation
Terraform has the limitation of not updating layers or lambda functions if
 no terraform code has chage. E.g you update your lambda code, but there is no
 need for tf update, in this case the terraform apply will not see this trigger.

This is an oppen issue and there is two workarounds:
1. Do a terraform destroy and then a terraform apply
2. Create a aws cli just to update the lambda and layer

## Layers
[Public layers](https://github.com/keithrozario/Klayers/tree/master/deployments/python3.8/arns)  
[Build a custom layer](https://stackoverflow.com/questions/46185297/using-numpy-in-aws-lambda)