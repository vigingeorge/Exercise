# run below commands to login to azure and connect to appropriate subscription for deployment

  az login
  az account set --subscription "subscription name"


# Command examples to run terraform scripts manually changing to appropriate enviroment

INIT `terraform init -backend-config "environments\[env]\config.azurerm.tfbackend"`

PLAN `terraform plan -var-file "environments\[env]\variables.tfvars"` 

APPLY `terraform apply -var-file "environments\[env]\variables.tfvars"` 