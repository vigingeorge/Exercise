## Run below commands to login to azure 

  az login
  
  az account set --subscription "subscription name"

## Command examples to run terraform scripts manually 

replace [env] below for the appropriate enviroment

INIT `terraform init -backend-config "environments\[env]\config.azurerm.tfbackend"`

PLAN `terraform plan -var-file "environments\[env]\variables.tfvars"` 

APPLY `terraform apply -var-file "environments\[env]\variables.tfvars"` 

