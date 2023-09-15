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

#Create the redis cache#
module "redis-cache" {
  source              = "./modules/redis-cache"
  project             = var.project
  environment         = var.environment
  team                = var.team
  instance            = var.instance
  location            = var.location
  resource_group_name = module.resource-group.name
}

#Create the private end point#
module "private-endpoint" {
  source                         = "./modules/private-endpoint"
  project                        = var.project
  environment                    = var.environment
  team                           = var.team
  instance                       = var.instance
  location                       = var.location
  resource_group_name            = module.resource-group.name
  subnet_id                      = module.subnet.id
  private_connection_resource_id = module.redis-cache.id
}
