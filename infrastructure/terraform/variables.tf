variable "subscription_id" { type = string }
variable "location" { type = string, default = "northeurope" }
variable "prefix" { type = string, default = "lakehouse-demo" }
variable "storage_account_name" { type = string, description = "Globally unique lowercase storage name, 3–24 characters" }
