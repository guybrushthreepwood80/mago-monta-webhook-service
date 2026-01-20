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

resource "aws_iam_policy" "lambda_dynamodb_write" {
  name        = "lambda_dynamodb_write_policy"
  description = "Allow Lamba to write to DynamoDB"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = ["dynamodb:PutItem"]
        Effect   = "Allow"
        Resource = aws_dynamodb_table.monta_webhooks.arn
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_attach_policy" {
  role       = aws_iam_role.iam_for_lambda.name 
  policy_arn = aws_iam_policy.lambda_dynamodb_write.arn
}