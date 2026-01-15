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