# Create Azure redis cache

resource "azurerm_redis_cache" "redis" {
  name                = "redis-${var.project}-${var.environment}-${var.team}-${var.instance}"
  location            = var.location
  resource_group_name = var.resource_group_name
  capacity            = var.capacity
  family              = var.family
  sku_name            = var.sku_name
  enable_non_ssl_port = var.enable_non_ssl_port
  minimum_tls_version = var.minimum_tls_version
  subnet_id           = var.use_vnet_injection ? var.subnet_id : null # Conditionally set the subnet_id
}