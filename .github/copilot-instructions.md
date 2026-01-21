# Copilot Instructions

This document outlines the standards and guidelines for using GitHub Copilot in this repository. Adhering to these instructions ensures consistency and quality across the codebase.

## General Guidelines
- Use clear and concise language in comments and documentation.
- Follow the repository's coding standards and conventions.
- Avoid generating code that violates security best practices.

## Language Standards
- All code comments and documentation must be in **English**.
- Terraform output descriptions must be in **English**.

### Python
- Follow [PEP 8](https://peps.python.org/pep-0008/) for code style.
- Use type hints wherever applicable.
- Write unit tests for all new functions and classes.
- Ensure compatibility with the specified Python version in the project.

### Terraform
- Follow the [Terraform Style Guide](https://www.terraform.io/docs/language/syntax/style.html).
- Use modules to organize resources logically.
- Always use `terraform fmt` to format code.
- Write clear and descriptive variable and resource names.
- Avoid hardcoding sensitive values; use environment variables or secret management tools.

## Documentation
- Use Markdown for documentation files.
- Include examples and usage instructions where applicable.
- Keep documentation up-to-date with code changes.

## Pull Requests
- Ensure all code is reviewed before merging.
- Include a clear description of changes in the pull request.
- Reference related issues or tasks.

By following these instructions, we can maintain a high standard of quality and collaboration in this project.