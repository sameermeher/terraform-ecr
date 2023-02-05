# Read the list of repository names from a file
data "template_file" "services_file" {
  template = file("repositories.txt")
}

locals {
  asset_id          = "a203843"
  repositories_list = split("\n", data.template_file.services_file.rendered)
}

# Convert the list into a map with key-value pairs
locals {
  repositories = {
    for r in local.repositories_list : r => r
  }
}

# Multiple ECR Repositories
module "ecr" {
  source   = "./modules/ecr"
  for_each = local.repositories

  name     = each.key
  asset_id = local.asset_id
}