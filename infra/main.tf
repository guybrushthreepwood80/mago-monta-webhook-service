#Terraform File
# Terraform 
terraform {
  backend "s3" {
    bucket = "mago-webhook-tf-state"
    key    = "prod/terraform.tfstate"
    region = "eu-west-3"
  }
}

# 1. Provider Konfiguration (Paris Region)
provider "aws" {
  region = "eu-west-3"
}

# 2. Archivierung des Python-Codes
# Terraform erstellt hier automatisch das ZIP-Paket für dich
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "../src/monta_webhook_handler.py"
  output_path = "monta_webhook_handler.zip"
}

# 3. IAM Rolle für die Lambda-Funktion
# Das ist die "Erlaubnis" für Lambda, als AWS-Dienst zu agieren
resource "aws_iam_role" "iam_for_lambda" {
  name = "monta_webhook_role_mago" # Hier kannst du dein Kürzel anhängen

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })

  tags = {
    Owner = "Martin Goth"
  }
}

# 4. Berechtigung für Logging
# Damit dein Lambda Nachrichten nach CloudWatch schreiben darf
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.iam_for_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# 5. Die Lambda Funktion
resource "aws_lambda_function" "webhook_lambda" {
  filename         = "monta_webhook_handler.zip"
  function_name    = "MontaWebhookHandler"
  role             = aws_iam_role.iam_for_lambda.arn
  
  # EXAKT: Dateiname (ohne .py) PUNKT Funktionsname
  handler          = "monta_webhook_handler.lambda_handler"
  
  runtime          = "python3.9"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  tags = {
    Owner = "Martin Goth"
    Project = "Monta-Webhook-Integration"
  }
}

# 6. API Gateway (Der "Eingang" aus dem Internet)
resource "aws_apigatewayv2_api" "lambda_api" {
  name          = "monta-webhook-api"
  protocol_type = "HTTP"
  
  tags = {
    Owner = "Martin Goth"
  }
}

# Verbindung zwischen API Gateway und Lambda
resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id           = aws_apigatewayv2_api.lambda_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.webhook_lambda.invoke_arn
}

# Die Route: Erlaubt POST-Anfragen auf den Pfad /webhook
resource "aws_apigatewayv2_route" "lambda_route" {
  api_id    = aws_apigatewayv2_api.lambda_api.id
  route_key = "POST /webhook"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

# Das "Stage" (Quasi die Live-Umgebung der API)
resource "aws_apigatewayv2_stage" "lambda_stage" {
  api_id      = aws_apigatewayv2_api.lambda_api.id
  name        = "$default"
  auto_deploy = true
}

# 7. Sicherheit: Erlaubt dem API Gateway explizit, dein Lambda aufzurufen
resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.webhook_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  
  # Zugriff einschränken auf diese spezifische API
  source_arn = "${aws_apigatewayv2_api.lambda_api.execution_arn}/*/*"
}

# 8. Output: Die URL, die du nach dem Push in GitHub Actions siehst
output "webhook_url" {
  description = "Die URL deines Webhooks"
  value       = "${aws_apigatewayv2_api.lambda_api.api_endpoint}/webhook"
}