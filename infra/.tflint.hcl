# Load the AWS ruleset plugin to check cloud-specific best practices
plugin "aws" {
    # Activate the AWS ruleset
    enabled = true
    # Use the official AWS plugin source
    source  = "github.com/terraform-linters/tflint-ruleset-aws"
    # Pin to a stable version of the plugin
    version = "0.32.0"
}

# Define the general linter behavior
config {
    # Use compact output for better readability in GitHub Actions
    format = "compact"
}

# Enforce versioning on S3 buckets (useful for State buckets)
rule "aws_s3_bucket_versioning" {
    # Flag any S3 bucket that does not have versioning enabled
    enabled = true
}