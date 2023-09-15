# Create resource group

resource "azurerm_resource_group" "rg" {
  name     = "rg-${var.project}-${var.environment}-${var.team}-${var.instance}"
  location = var.location
  tags     = var.common_tags
}