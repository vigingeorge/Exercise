# Create private end point
resource "azurerm_private_endpoint" "pe" {
  name                = "pep-${var.project}-${var.environment}-${var.team}-${var.instance}"
  location            = var.location
  resource_group_name = var.resource_group_name
  subnet_id           = var.subnet_id

  private_service_connection {
    name                           = "PrivateServiceConnection"
    is_manual_connection           = false
    private_connection_resource_id = var.private_connection_resource_id
    subresource_names              = ["redisCache"]
  }
}