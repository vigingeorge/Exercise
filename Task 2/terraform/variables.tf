variable "project" {
  description = "The project name associated with the resources."
  default     = "myproject"
}

variable "environment" {
  description = "The environment name associated with the resources."
  default     = "dev"
}

variable "team" {
  description = "The team name associated with the resources."
  default     = "avengers"
}

variable "instance" {
  description = "The instance number or identifier."
  default     = "001"
}

variable "location" {
  description = "The Azure region where resources will be deployed."
  default     = "westeurope"
}

variable "common_tags" {
  description = "Common tags to apply to Azure resources."
  default     = {
    Environment  = "development",
    ITSystemCode = "batman",
    Responsible  = "John Doe"
  }
}

variable "vnet_address_space" {
  description = "The address space for the Virtual Network (VNet)."
  default     = "10.0.0.0/16"
}

variable "sub_address_prefix" {
  description = "The address prefix for the subnet within the VNet."
  default     = "10.0.1.0/24"
}

variable "subnet_name" {
  description = "The name of the subnet within the VNet."
  default     = "subnet"
}
