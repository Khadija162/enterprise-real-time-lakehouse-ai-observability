# Azure + Meta Llama deployment roadmap

## Components

| Capability | Azure service |
|---|---|
| Kafka-compatible ingestion | Azure Event Hubs |
| Distributed Spark and Delta | Azure Databricks |
| Data lake and checkpoints | Azure Data Lake Storage Gen2 |
| Operational incidents/metadata | Azure Database for PostgreSQL |
| FastAPI backend | Azure Container Apps |
| Next.js frontend | Azure Static Web Apps or Container Apps |
| Llama inference | Microsoft Foundry model endpoint (availability varies by subscription and region) |
| Secrets and identity | Azure Key Vault, managed identities, Microsoft Entra ID |
| Telemetry | Azure Monitor / Application Insights |

## Safety and implementation order

1. Develop FastAPI and Next.js locally using mock inference and synthetic data.
2. Verify monitoring contracts and report schemas; migrate SQLite reports to Azure PostgreSQL.
3. Provision Event Hubs and ADLS with least-privilege access.
4. Run Delta jobs on Databricks and publish consistent metrics snapshots.
5. Create a Foundry deployment **only if** the desired Meta Llama model is supported in your region.
6. Set LLAMA_MODE=azure, AZURE_LLAMA_ENDPOINT (provider chat-completions endpoint), AZURE_LLAMA_MODEL and secret AZURE_LLAMA_API_KEY in server-side settings.
7. Deploy API and frontend; add OIDC authentication before any public release.
8. Add CI/CD, cost limits, alert notifications and incident evaluation tests.

**Never expose model keys in browser code.** The included starter API has no authentication and must not be exposed publicly. The Terraform folder is an example module for an Azure resource group and storage; it does not create the entire platform.
