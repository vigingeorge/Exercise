variable "project" {
  default = ""
}

variable "environment" {
  default = "dev"
}

variable "team" {
  default = "aops"
}

variable "instance" {
  default = "001"
}

variable "location" {
  default = "westeurope"
}

variable "resource_group_name" {
  default = ""
}

variable "common_tags" {
  default = {
    Environment  = "Dev",
    ITSystemCode = "",
    Responsible  = ""
  }
}

variable "vnet_address_space" {}

variable "sub_address_prefix" {}

variable "subnet_name" {}