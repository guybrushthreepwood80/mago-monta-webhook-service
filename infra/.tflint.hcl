# Load the AWS ruleset plugin
plugin "aws" {
    enabled = true
    version = "0.32.0"
    source  = "github.com/terraform-linters/tflint-ruleset-aws"
}

# Global TFLint configuration
config {
    format = "compact"
}

# Version-specific checks must be in this block
terraform {
    enabled = true
    preset  = "recommended"
    # Moved terraform_version here
    terraform_version = "1.5.0"
}

# S3 security rule
rule "aws_s3_bucket_versioning" {
    enabled = true
}