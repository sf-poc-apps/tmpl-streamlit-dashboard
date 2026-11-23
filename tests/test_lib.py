import io
import pathlib

from lib import load_csv, summarize

SAMPLE = pathlib.Path(__file__).resolve().parent.parent / "data" / "sample.csv"


def test_sample_loads():
    df = load_csv(SAMPLE)
    assert list(df.columns) == ["date", "category", "amount"]


def test_summarize_groups():
    df = load_csv(io.StringIO("Category,Amount\nA,1\nB,2\nA,3\n"))
    s = summarize(df, "amount", "category")
    assert s["total"] == 6.0
    assert s["by_group"] == {"A": 4.0, "B": 2.0}


def test_banner_present():
    app = (SAMPLE.parent.parent / "app.py").read_text()
    assert "sf-banner" in app
