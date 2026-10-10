import pytest
from monitoring.quality_rules import calculate_metrics, evaluate_quality


def test_healthy():
    assert evaluate_quality(calculate_metrics(100, 100, 0, 0)) == []


def test_rejection_alert():
    alerts = evaluate_quality(calculate_metrics(100, 90, 10, 0))
    assert any(a["rule"] == "HIGH_REJECTION_RATE" for a in alerts)


def test_reconciliation():
    with pytest.raises(ValueError, match="reconcile"):
        calculate_metrics(100, 90, 20, 0)
