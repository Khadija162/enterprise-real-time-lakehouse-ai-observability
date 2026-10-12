terraform {
  required_version = ">= 1.6.0"
  required_providers {
    azurerm = { source = "hashicorp/azurerm", version = "~> 4.0" }
  }
}
provider "azurerm" { features {} subscription_id = var.subscription_id }
resource "azurerm_resource_group" "lakehouse" {
  name = "${var.prefix}-rg"
  location = var.location
}
resource "azurerm_storage_account" "lakehouse" {
  name = var.storage_account_name
  resource_group_name = azurerm_resource_group.lakehouse.name
  location = azurerm_resource_group.lakehouse.location
  account_tier = "Standard"
  account_replication_type = "LRS"
  is_hns_enabled = true
  min_tls_version = "TLS1_2"
  allow_nested_items_to_be_public = false
}
resource "azurerm_storage_data_lake_gen2_filesystem" "data" {
  name = "lakehouse"
  storage_account_id = azurerm_storage_account.lakehouse.id
}
output "storage_account_name" { value = azurerm_storage_account.lakehouse.name }
