import pandas as pd
import pytest
from pipelines.etl_pipeline import validate_orders


def test_clean_and_rejected_rows():
    df = pd.DataFrame([
        {"order_id": 1, "customer_id": 2, "product": "Laptop", "amount": 100},
        {"order_id": 1, "customer_id": 2, "product": "Laptop", "amount": 100},
        {"order_id": 3, "customer_id": 4, "product": "Mouse", "amount": -5},
        {"order_id": 4, "customer_id": 5, "product": "Phone", "amount": None},
    ])
    clean, rejected = validate_orders(df)
    assert len(clean) == 1
    assert len(rejected) == 3
    assert clean["amount"].sum() == 100
    assert "Duplicate order ID" in rejected["rejection_reason"].iloc[0]


def test_missing_columns_fails():
    with pytest.raises(ValueError, match="Missing columns"):
        validate_orders(pd.DataFrame({"order_id": [1]}))
