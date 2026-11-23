"""Data helpers kept separate from the Streamlit UI so they can be unit tested."""
import pandas as pd

MAX_ROWS = 50_000


def load_csv(source) -> pd.DataFrame:
    df = pd.read_csv(source, nrows=MAX_ROWS)
    df.columns = [str(c).strip().lower() for c in df.columns]
    return df


def summarize(df: pd.DataFrame, value_col: str, group_col: str) -> dict:
    if value_col not in df or group_col not in df:
        return {"rows": len(df), "total": 0.0, "by_group": {}}
    values = pd.to_numeric(df[value_col], errors="coerce").fillna(0)
    by_group = values.groupby(df[group_col].astype(str)).sum().sort_values(ascending=False)
    return {"rows": len(df), "total": float(values.sum()), "by_group": {k: float(v) for k, v in by_group.items()}}
