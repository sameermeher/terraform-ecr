variable "name" {
  type = string
  description = "(Required) Name of the repository. {asset_id}/{name}."
}

variable "asset_id" {
  type = string
  description = "(Required) Project name of the repository. {asset_id}/{name}."
}

variable "default_tags" {
  type = map(string)
  default = {
    environment = "development"
    iaac-tool   = "terraform"
    contact     = "abc@gmail.com"
  }
}

variable "expiration_after_days" {
  type = number
  description = "(Optional) Delete images older than X days."
  default = 60
}