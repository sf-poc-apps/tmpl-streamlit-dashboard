import os
import pathlib

import pandas as pd
import streamlit as st

from lib import load_csv, summarize

st.set_page_config(page_title="Dashboard", layout="wide")

# sf-banner: required POC banner. Do not remove.
expires = os.environ.get("SF_EXPIRES", "")[:10] or "soon"
st.markdown(
    f"<div id='sf-banner' style='background:#4b1f7a;color:#fff;padding:6px 12px;border-radius:6px;"
    f"font-weight:600;text-align:center'>POC built by an AI software factory - expires on {expires}. "
    f"Do not upload personal or confidential data.</div>",
    unsafe_allow_html=True,
)

st.title("Dashboard")
uploaded = st.file_uploader("Upload a CSV (max 5 MB)", type=["csv"])
sample = pathlib.Path(__file__).parent / "data" / "sample.csv"
df: pd.DataFrame = load_csv(uploaded if uploaded is not None else sample)
st.caption("Using uploaded file" if uploaded is not None else "Using bundled sample data")

stats = summarize(df, value_col="amount", group_col="category")
c1, c2, c3 = st.columns(3)
c1.metric("Rows", stats["rows"])
c2.metric("Total", f"{stats['total']:,.2f}")
c3.metric("Groups", len(stats["by_group"]))
st.bar_chart(pd.Series(stats["by_group"], name="amount"))
st.dataframe(df, use_container_width=True)
