# URL Shortener — Cloud-Native Deployment

A simple URL shortener web application demonstrating a full cloud-native deployment pipeline: Infrastructure as Code (Terraform), CI/CD (GitHub Actions), and a managed PaaS deployment on Microsoft Azure.

🔗 **Live App:** https://url-shortener-asmar.azurewebsites.net

---

## Architecture

Browser → Azure App Service (Flask app) → Azure PostgreSQL Flexible Server

**Stack:**
- **Frontend:** HTML (Flask templates)
- **Backend:** Python / Flask
- **Database:** PostgreSQL (Azure Flexible Server)
- **Infrastructure as Code:** Terraform
- **CI/CD:** GitHub Actions
- **Cloud Platform:** Microsoft Azure

---

## Application Features

- Paste a long URL and get a short code back
- Visiting the short URL redirects to the original
- All URLs stored in a PostgreSQL database

---

## Cloud Infrastructure (Terraform)

All infrastructure is provisioned with a single command: `terraform apply`

The Terraform configuration (`/terraform`) creates:

| Resource | Purpose |
|---|---|
| Resource Group | Logical container for all resources |
| App Service Plan (Linux, B1) | Compute tier for hosting the web app |
| Linux Web App | Runs the Flask application (Python 3.11) |
| PostgreSQL Flexible Server | Managed database (B_Standard_B1ms) |
| PostgreSQL Database | The `urlshortener` database |
| Firewall Rule | Allows Azure services to access the database |

### Why these choices?

- **Azure App Service (PaaS)** was chosen over a VM because it requires no OS management, supports automatic deployment from GitHub Actions out of the box, and scales easily — appropriate for a small web app like this.
- **Azure PostgreSQL Flexible Server (DBaaS)** was chosen over running PostgreSQL in a VM because it provides automated backups, patching, and high availability without manual maintenance.
- **Terraform** was chosen as the IaC tool because it is cloud-agnostic, has a large provider ecosystem, and uses a declarative syntax that makes infrastructure easy to review and version.

### Provisioning the Infrastructure

\`\`\`bash
cd terraform
terraform init
terraform apply
\`\`\`

Outputs after apply:
- `app_url` — the public URL of the deployed application
- `db_server_fqdn` — the PostgreSQL server hostname

---

## CI/CD Pipeline (GitHub Actions)

The pipeline is defined in `.github/workflows/deploy.yml` and triggers automatically on every push to `main`.

### Pipeline Steps

1. **Checkout code** — pulls the latest code from the repository
2. **Set up Python 3.11**
3. **Install dependencies** from `requirements.txt`
4. **Run tests** with `pytest`
5. **Login to Azure** using a service principal stored as a GitHub secret (`AZURE_CREDENTIALS`)
6. **Deploy to Azure App Service** using `azure/webapps-deploy`

### How It Ensures Automatic Deployment

Any code pushed to the `main` branch automatically triggers this pipeline. If tests pass, the updated code is deployed directly to the live Azure App Service — no manual steps required.

---

## Local Development

\`\`\`bash
git clone https://github.com/AsmarBaghirova/url-shortener.git
cd url-shortener

python -m venv venv
venv\\Scripts\\activate

pip install -r requirements.txt

# Set up .env file with your local PostgreSQL connection string
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/urlshortener

python app.py
\`\`\`

---

## Testing

\`\`\`bash
pytest test_app.py -v
\`\`\`

---

## Project Structure

- app.py — Flask application
- test_app.py — Tests
- requirements.txt — Python dependencies
- startup.sh — Azure startup command
- templates/index.html — Frontend
- terraform/main.tf — Infrastructure definition
- terraform/variables.tf — Configurable variables
- terraform/outputs.tf — Output values
- .github/workflows/deploy.yml — CI/CD pipeline