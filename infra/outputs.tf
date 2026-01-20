# infra/outputs.tf

output "webhook_url" {
  # Deine Ressource heißt "lambda_stage", nicht "default"
  value       = "${aws_apigatewayv2_stage.lambda_stage.invoke_url}/webhook"
  description = "Die URL für das Monta Webhook-Dashboard."
}

output "dynamodb_table_name" {
  # Deine Ressource heißt "monta_webhooks", nicht "webhook_events"
  value       = aws_dynamodb_table.monta_webhooks.name
  description = "Der Name der DynamoDB Tabelle."
}