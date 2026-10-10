# Enterprise Real-Time Lakehouse with AI Data Observability

A beginner-friendly, learning-to-production data engineering project covering Python ETL, data quality, PostgreSQL, Spark, Delta Lake, Kafka, monitoring and AI incident triage.

> **Current repository status:** Starter implementation. The Python/Pandas ETL, quarantined records, quality rules and unit tests are included and runnable. Later lessons (PostgreSQL, Kafka, Delta, AI) are documented in the roadmap but their code is **not yet included**.

## Architecture roadmap

```text
Source CSV / databases / Kafka
            ↓
      Python / streaming ingestion
            ↓
        Bronze (raw)
            ↓
    Validation + rejected records
            ↓
       Silver (clean data)
            ↓
       Gold (analytics)
            ↓
      Metrics + alerts
            ↓
 AI investigation (human reviewed)
```

## Run locally on Windows

Requires Python 3.11 or 3.12. Open PowerShell inside the project folder:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe pipelines\etl_pipeline.py
.\.venv\Scripts\python.exe -m pytest -q
```

Sample results are written to `data/processed/`, which is excluded from Git.

## Included files

- `pipelines/etl_pipeline.py`: CSV extraction, validation and clean/rejected outputs
- `monitoring/quality_rules.py`: quality metrics and alert thresholds
- `tests/`: automated Python tests
- `data/raw/orders.csv`: synthetic eight-row example
- `docs/architecture.md`: architecture notes
- `.gitignore`: protects local credentials, generated data and checkpoints

## Roadmap

- [x] Batch ETL in Pandas with quarantined invalid records
- [x] Data-quality rules and tests
- [ ] PostgreSQL UPSERT + run history
- [ ] PySpark + Bronze/Silver/Gold Parquet
- [ ] Delta Lake MERGE and history
- [ ] Docker/Kafka producer and consumer
- [ ] Spark Structured Streaming and checkpoints
- [ ] Observability metrics and incident reporting
- [ ] Read-only AI incident analysis
- [ ] CI/CD, cloud deployment, security and performance testing

## Safety

Only synthetic example data belongs in this repository. Never commit API keys, passwords, customer data, local databases, generated Parquet/Delta datasets or checkpoints.

## License

MIT. See [LICENSE](LICENSE).
