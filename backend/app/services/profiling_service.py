import json


def profile_dataframe(df):
    total_rows = len(df)
    columns = []
    total_missing = 0

    for name in df.columns:
        series = df[name]
        missing = int(series.isna().sum())
        total_missing += missing
        percent = round(missing / total_rows * 100, 2) if total_rows else 0.0
        columns.append({
            "name": str(name),
            "dtype": str(series.dtype),
            "missing": missing,
            "missing_pct": percent,
            "unique": int(series.nunique()),
        })

    statistics = {}
    numeric = df.select_dtypes(include="number")
    if numeric.shape[1] > 0:
        # to_json turns NaN into null so the API response is valid JSON
        statistics = json.loads(numeric.describe().to_json())

    return {
        "rows": total_rows,
        "columns_count": int(df.shape[1]),
        "total_missing": total_missing,
        "duplicate_rows": int(df.duplicated().sum()),
        "columns": columns,
        "statistics": statistics,
    }


def preview_dataframe(df, rows=20):
    head = df.head(rows)
    data = json.loads(head.to_json(orient="split", date_format="iso"))
    return {
        "columns": [str(c) for c in data["columns"]],
        "rows": data["data"],
        "total_rows": len(df),
    }
