# infra/outputs.tf

output "webhook_url" {
  value       = "${aws_apigatewayv2_stage.lambda_stage.invoke_url}/webhook"
  description = "The URL for the Monta Webhook dashboard. Copy this URL into your Monta account."
}

output "dynamodb_table_name" {
  value       = aws_dynamodb_table.monta_webhooks.name
  description = "The name of the DynamoDB table where events are stored."
}