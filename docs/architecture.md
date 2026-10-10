# Architecture notes

This starter intentionally separates the **implemented batch ETL** from planned streaming/lakehouse components.

## Planned pipeline

1. Kafka holds event streams with stable event IDs and offsets.
2. Spark Structured Streaming captures immutable events in Bronze Delta.
3. Silver validates, quarantines errors, and deduplicates using stable keys.
4. Gold computes business metrics based on current order state.
5. A monitoring service tracks data quality, freshness, reconciliation and failures.
6. An AI service provides **read-only** incident triage with evidence and hypotheses separated.

## Open design questions

- CDC event ordering and update/cancel semantics
- Checkpoint and sink recovery strategy
- Schema compatibility and data contracts
- PII policy, retention, access controls
- Cloud cost and pipeline SLOs
