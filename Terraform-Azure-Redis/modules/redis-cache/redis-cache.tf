# Create Azure redis cache

resource "azurerm_redis_cache" "redis" {
  name                = "redis-${var.project}-${var.environment}-${var.team}-${var.instance}"
  location            = var.location
  resource_group_name = var.resource_group_name
  capacity            = 0
  family              = "C"
  sku_name            = "Basic"
  enable_non_ssl_port = false
  minimum_tls_version = "1.2"
}