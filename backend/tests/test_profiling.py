from pathlib import Path
import pandas as pd
from app.services.profiling_service import profile_dataframe, preview_dataframe


def test_profile_missing_and_duplicates():
    df = pd.DataFrame({"a": [1, 2, 2, None], "b": ["x", "y", "y", "z"]})
    p = profile_dataframe(df)
    assert p["rows"] == 4
    assert p["columns_count"] == 2
    assert p["total_missing"] == 1
    assert p["duplicate_rows"] == 1
    assert p["columns"][0]["missing"] == 1
    assert "a" in p["statistics"] and "b" not in p["statistics"]


def test_profile_empty_dataframe():
    p = profile_dataframe(pd.DataFrame({"a": []}))
    assert p["rows"] == 0
    assert p["columns"][0]["missing_pct"] == 0.0


def test_preview_converts_nan_to_none():
    df = pd.DataFrame({"a": [1.0, None]})
    p = preview_dataframe(df, 5)
    assert p["rows"][1][0] is None
    assert p["total_rows"] == 2


def test_sample_dataset_has_issues():
    path = Path(__file__).resolve().parents[2] / "sample_data" / "sales_small.csv"
    df = pd.read_csv(path)
    p = profile_dataframe(df)
    assert p["duplicate_rows"] > 0
    assert p["total_missing"] > 0
