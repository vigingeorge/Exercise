# Create vnet

resource "azurerm_virtual_network" "vnet" {
  name                = "vnet-${var.project}-${var.environment}-${var.team}-${var.instance}"
  location            = var.location
  resource_group_name = var.resource_group_name
  address_space       = var.vnet_address_space
}