# Enterprise Real-Time Lakehouse with AI Data Observability

An **Azure-ready full-stack data engineering portfolio project** combining Python ETL, data-quality monitoring, a FastAPI control plane, a Next.js dashboard and **Meta Llama** incident triage.

> **Implementation status:** The Python/Pandas ETL and quality rules, FastAPI API, minimal Next.js dashboard, mocked AI service, tests, and an Azure Terraform example are implemented. Full Kafka/Event Hubs ingestion, Databricks/Delta deployment, cloud PostgreSQL, authentication and live Llama deployment are planned — not yet running in Azure.

## Architecture

```text
Synthetic e-commerce data
  -> Python ETL (implemented) / Azure Event Hubs (planned)
  -> Spark + Delta Bronze / Silver / Gold (planned cloud integration)
  -> Monitoring database (Lesson 9 integration expected)
  -> FastAPI API -> Next.js dashboard
                -> Llama incident triage (mock by default / Azure endpoint optional)
```

See [Azure deployment plan](docs/azure-deployment.md) and [architecture notes](docs/architecture.md).

## Windows quick start

### Python ETL and tests

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -r backend/requirements.txt
.\.venv\Scripts\python.exe pipelines\etl_pipeline.py
.\.venv\Scripts\python.exe -m pytest tests backend/tests -q
```

### FastAPI (terminal 1)

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload
```

Open http://127.0.0.1:8000/docs for API docs. If you haven't completed Lesson 9, metrics and alerts are empty (not fabricated).

### Next.js (terminal 2)

Requires a recent supported Node.js LTS release. From repository root:

```powershell
cd frontend
npm install
npm run dev
```

Open http://localhost:3000. Server-side Next.js reads backend from `API_BASE_URL` (defaults to http://127.0.0.1:8000).

### AI incident analyzer

By default `LLAMA_MODE=mock` and **no Azure API key is required**. POST `/api/ai/analyze` with a real `run_id` recorded in the monitoring SQLite database. For a real Foundry deployment set `LLAMA_MODE=azure`, `AZURE_LLAMA_ENDPOINT`, `AZURE_LLAMA_MODEL` and `AZURE_LLAMA_API_KEY` **server-side**. Confirm that your endpoint supports an OpenAI-compatible chat completions API and the deployed model is available in your region.

**Security:** The sample API has no authentication; run on localhost only. Do not publish this backend or sensitive pipeline details on a public host until authentication/authorization and data sanitization are implemented.

## Project folders

- `backend/` — FastAPI routes and mockable Llama adapter
- `frontend/` — Next.js status dashboard
- `pipelines/` — ETL starter
- `monitoring/` — reusable data-quality calculations
- `infrastructure/terraform/` — small Azure resource-group and ADLS example; **not** a full deployment
- `tests/`, `backend/tests/` — tests
- `docs/` — architecture and Azure deployment guidance

## Remaining milestones

- [x] Batch ETL and tests
- [x] Backend API and dashboard skeleton
- [x] Mock AI incident triage
- [x] CI workflow and starter Azure IaC
- [ ] Wire actual monitoring metrics and alert history
- [ ] Kafka/Event Hubs + Spark/Delta integration
- [ ] Azure PostgreSQL and identity management
- [ ] Deploy Llama via Microsoft Foundry
- [ ] Authentication, performance testing, and production hardening

MIT license. Use synthetic records only; credentials and generated data are ignored by Git.
