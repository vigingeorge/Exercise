#Create the resource group#
module "resource-group" {
  source      = "./modules/resource-group"
  project     = var.project
  environment = var.environment
  team        = var.team
  instance    = var.instance
  common_tags = var.common_tags
  location    = var.location
}

#Create the vnet#
module "vnet" {
  source              = "./modules/vnet"
  project             = var.project
  environment         = var.environment
  team                = var.team
  instance            = var.instance
  location            = var.location
  resource_group_name = module.resource-group.name
  vnet_address_space  = var.vnet_address_space
}

#Create the subnet#
module "subnet" {
  source              = "./modules/subnet"
  subnet_name         = var.subnet_name
  resource_group_name = module.resource-group.name
  vnet_name           = module.vnet.name
  sub_address_prefix  = var.sub_address_prefix
}

#Create the redis cache 
module "redis-cache" {
  source = "./modules/redis-cache"
  project             = var.project
  environment         = var.environment
  team                = var.team
  instance            = var.instance
  location            = var.location
  capacity            = var.capacity
  family              = var.family
  sku_name            = var.sku_name
  enable_non_ssl_port = var.enable_non_ssl_port
  minimum_tls_version = var.minimum_tls_version
  resource_group_name = module.resource-group.name
  subnet_id           = module.subnet.id
  use_vnet_injection  = var.use_vnet_injection
}


#Create the private end point#
module "private-endpoint" {
  source                         = "./modules/private-endpoint"
  count                          = var.use_vnet_injection ? 0 : 1
  project                        = var.project
  environment                    = var.environment
  team                           = var.team
  instance                       = var.instance
  location                       = var.location
  resource_group_name            = module.resource-group.name
  subnet_id                      = module.subnet.id
  private_connection_resource_id = module.redis-cache.id
}
