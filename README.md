# Mago Monta Webhook Service 🚀

Ein serverloser Service zur Verarbeitung von Webhooks der Monta-Plattform. Dieses Projekt dient als technische Demonstration für ein robustes AWS-Setup mit **Terraform** und **GitHub Actions**.

## 🛠 Tech Stack
* **Cloud:** AWS (Lambda, API Gateway, DynamoDB)
* **IaC:** Terraform
* **Sprache:** Python 3.9+
* **CI/CD:** GitHub Actions

## 🏗 Architektur
Der Service empfängt Webhook-Events von Monta über ein **API Gateway**, validiert die Daten in einer **Lambda-Funktion** und speichert die Transaktions-Logs in einer **DynamoDB-Tabelle**.

## 🚀 Deployment
Die Infrastruktur wird automatisch via GitHub Actions ausgerollt, sobald ein Push auf den `main` Branch erfolgt.

```bash
# Lokales Testen der Terraform-Konfiguration
cd infra
terraform init
terraform plan
```

## 📧 Email Notifications
The repository includes an automated email notification workflow that sends alerts when:
- A push is made to any branch
- A pull request is opened targeting the main branch

### Setup Instructions
To enable email notifications, configure the following GitHub repository secrets:

1. Go to repository **Settings** → **Secrets and variables** → **Actions**
2. Add the following secrets:
   - `EMAIL_USERNAME`: SMTP username (e.g., your Gmail address)
   - `EMAIL_PASSWORD`: SMTP password (for Gmail, use an App Password)

#### Creating a Gmail App Password
1. Enable 2-factor authentication on your Google account
2. Visit https://myaccount.google.com/apppasswords
3. Create a new app password for "Mail"
4. Use this password as `EMAIL_PASSWORD` in GitHub secrets

The workflow is configured to send notifications to `goth.martin@gmail.com`