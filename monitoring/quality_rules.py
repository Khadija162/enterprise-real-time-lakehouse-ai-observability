"""Pure quality metric calculations; no Spark required."""


def calculate_metrics(bronze_count, silver_count, rejected_count, duplicate_count):
    counts = (bronze_count, silver_count, rejected_count, duplicate_count)
    if any(not isinstance(n, int) or isinstance(n, bool) or n < 0 for n in counts):
        raise ValueError("Counts must be non-negative integers")
    if silver_count + rejected_count + duplicate_count != bronze_count:
        raise ValueError("Event counts do not reconcile")
    return {
        "bronze_count": bronze_count,
        "silver_count": silver_count,
        "rejected_count": rejected_count,
        "duplicate_count": duplicate_count,
        "rejection_rate": round(100 * rejected_count / bronze_count, 2) if bronze_count else 0.0,
        "duplicate_rate": round(100 * duplicate_count / bronze_count, 2) if bronze_count else 0.0,
    }


def evaluate_quality(metrics):
    alerts = []
    if metrics["bronze_count"] == 0:
        alerts.append({"severity": "WARNING", "rule": "EMPTY_BRONZE"})
    if metrics["rejection_rate"] > 5:
        alerts.append({"severity": "CRITICAL", "rule": "HIGH_REJECTION_RATE"})
    if metrics["duplicate_rate"] > 10:
        alerts.append({"severity": "WARNING", "rule": "HIGH_DUPLICATE_RATE"})
    return alerts
