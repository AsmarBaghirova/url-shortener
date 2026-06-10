variable "resource_group_name" {
  default = "url-shortener-rg"
}

variable "location" {
  default = "westeurope"
}

variable "app_service_plan_name" {
  default = "url-shortener-plan"
}

variable "app_service_name" {
  default = "url-shortener-asmar"
}

variable "db_server_name" {
  default = "url-shortener-db-asmar"
}

variable "db_name" {
  default = "urlshortener"
}

variable "db_username" {
  default = "psqladmin"
}

variable "db_password" {
  sensitive = true
}