# infra/outputs.tf

output "webhook_url" {
  value       = "${aws_apigatewayv2_stage.default.invoke_url}/webhook"
  description = "URL for Webhook Endpoint"
}

output "dynamodb_table_name" {
  value       = aws_dynamodb_table.webhook_events.name
  description = "Name of DynamoDB Table for storing webhook events"
}