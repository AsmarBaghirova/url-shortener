output "app_url" {
  value = "https://${azurerm_linux_web_app.app.default_hostname}"
}

output "db_server_fqdn" {
  value = azurerm_postgresql_flexible_server.db.fqdn
}