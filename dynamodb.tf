resource "aws_dynamodb_table" "monta_webhooks" {
  name           = "monta_webhook_events"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "id"

  attribute {
    name = "id"
    type = "S"
  }

  tags = {
    Project = "Mago-Monta"
    Feature = "Webhook-Storage"
  }
}