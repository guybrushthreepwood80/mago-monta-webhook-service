# Main entry point for Terraform configuration
terraform {
  # Define the minimum Terraform CLI version required
  required_version = ">= 1.5.0"

  # Secure state storage in S3
  backend "s3" {
    bucket = "mago-webhook-tf-state"
    key    = "prod/terraform.tfstate"
    region = "eu-west-3"
    encrypt = true
  }

  # Specify and lock provider versions for stability
  required_providers {
    # AWS provider for infrastructure resources
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
    # Archive provider for zipping Lambda code
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4"
    }
  }
}

# Regional configuration for AWS
provider "aws" {
  region = "eu-west-3"
}

# Create the deployment package from source code
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "../src/monta_webhook_handler.py"
  output_path = "monta_webhook_handler.zip"
}

# Execution role for the Lambda function
resource "aws_iam_role" "iam_for_lambda" {
  name = "monta_webhook_role_mago"

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

# Attach basic logging permissions to the role
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.iam_for_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Main Lambda function resource
resource "aws_lambda_function" "webhook_lambda" {
  filename      = "monta_webhook_handler.zip"
  function_name = "MontaWebhookHandler"
  role          = aws_iam_role.iam_for_lambda.arn

  handler = "monta_webhook_handler.lambda_handler"


  runtime          = "python3.12"

  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  tags = {
    Owner   = "Martin Goth"
    Project = "Monta-Webhook-Integration"
  }
}

# HTTP API Gateway for the public endpoint
resource "aws_apigatewayv2_api" "lambda_api" {
  name          = "monta-webhook-api"
  protocol_type = "HTTP"

  tags = {
    Owner = "Martin Goth"
  }
}

# Connect the API Gateway to the Lambda function
resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id           = aws_apigatewayv2_api.lambda_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.webhook_lambda.invoke_arn
}

# Define the POST route for incoming webhooks
resource "aws_apigatewayv2_route" "lambda_route" {
  api_id    = aws_apigatewayv2_api.lambda_api.id
  route_key = "POST /webhook"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

# Deployment stage for the API
resource "aws_apigatewayv2_stage" "lambda_stage" {
  api_id      = aws_apigatewayv2_api.lambda_api.id
  name        = "$default"
  auto_deploy = true
}

# Permissions for API Gateway to trigger the Lambda
resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.webhook_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.lambda_api.execution_arn}/*/*"
}

#