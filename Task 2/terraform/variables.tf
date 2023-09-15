variable "project" {
  default = ""
}

variable "environment" {
  default = ""
}

variable "team" {
  default = ""
}

variable "instance" {
  default = "001"
}

variable "location" {
  default = "westeurope"
}


variable "common_tags" {
  default = {
    Environment  = "",
    ITSystemCode = "",
    Responsible  = ""
  }
}

variable "vnet_address_space" {
  default = ""
}

variable "sub_address_prefix" {
  default = ""
}

variable "subnet_name" {
  default = ""
}