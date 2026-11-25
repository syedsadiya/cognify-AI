from app.db.models import Dataset, BenchmarkRun, EngineMetric


def test_relationships(session_factory):
    db = session_factory()
    ds = Dataset(original_name="sales.csv", stored_name="abc123.csv", file_type="csv")
    db.add(ds)
    db.commit()

    run = BenchmarkRun(dataset_id=ds.id, operation="group_agg")
    db.add(run)
    db.commit()

    db.add(EngineMetric(run_id=run.id, engine="polars", median_time_ms=12.5))
    db.commit()

    saved = db.query(BenchmarkRun).first()
    assert saved.dataset.original_name == "sales.csv"
    assert saved.metrics[0].engine == "polars"
    db.close()
