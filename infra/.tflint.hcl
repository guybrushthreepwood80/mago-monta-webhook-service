# Load the AWS ruleset plugin to check cloud-specific best practices
plugin "aws" {
    # Activate the AWS ruleset for TFLint
    enabled = true
    # Use the official AWS plugin source
    source  = "github.com/terraform-linters/tflint-ruleset-aws"
    # Pin to a stable version of the plugin
    version = "0.32.0"
}

# Define the general linter behavior and environment
config {
    # Check compatibility with your specific Terraform version
    terraform_version = "1.5.0"
    # Use compact output for better readability in GitHub Actions
    format = "compact"
}

# Enforce versioning on S3 buckets to prevent data loss (e.g., in your State-Bucket)
rule "aws_s3_bucket_versioning" {
    # Flag any S3 bucket that does not have versioning enabled
    enabled = true
}