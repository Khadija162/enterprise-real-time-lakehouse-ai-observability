"""Basic repeatable ETL for synthetic e-commerce orders."""
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
COLUMNS = ["order_id", "customer_id", "product", "amount"]


def validate_orders(source: pd.DataFrame):
    missing = set(COLUMNS) - set(source.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    df = source.copy()
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    reasons = pd.Series("", index=df.index, dtype="string")

    def add(mask, reason):
        nonlocal reasons
        reasons.loc[mask] = reasons.loc[mask] + reason + "; "

    add(df["order_id"].isna(), "Missing order ID")
    add(df["customer_id"].isna(), "Missing customer ID")
    add(df["product"].isna() | df["product"].astype("string").str.strip().eq("").fillna(False), "Missing product")
    add(df["amount"].isna(), "Missing or invalid amount")
    add(df["amount"].notna() & df["amount"].le(0), "Non-positive amount")
    add(df["order_id"].notna() & df["order_id"].duplicated(keep="first"), "Duplicate order ID")

    invalid = reasons.ne("")
    clean = df.loc[~invalid].copy()
    rejected = df.loc[invalid].copy()
    rejected["rejection_reason"] = reasons.loc[invalid].str.rstrip("; ")
    return clean, rejected


def run_pipeline():
    raw = pd.read_csv(BASE / "data" / "raw" / "orders.csv")
    clean, rejected = validate_orders(raw)
    output = BASE / "data" / "processed"
    output.mkdir(parents=True, exist_ok=True)
    clean.to_csv(output / "clean_orders.csv", index=False)
    rejected.to_csv(output / "rejected_orders.csv", index=False)
    pd.DataFrame([{"raw_records": len(raw), "clean_records": len(clean), "rejected_records": len(rejected), "total_sales": clean["amount"].sum()}]).to_csv(output / "sales_summary.csv", index=False)
    print(f"Raw: {len(raw)} | Clean: {len(clean)} | Rejected: {len(rejected)} | Sales: {clean['amount'].sum():.2f}")


if __name__ == "__main__":
    run_pipeline()
