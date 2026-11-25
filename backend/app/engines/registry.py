import importlib
import importlib.util

ENGINE_MODULES = {
    "pandas": "pandas",
    "polars": "polars",
    "duckdb": "duckdb",
    "fireducks": "fireducks",
}


def engine_status() -> list:
    """Report which engines are installed. FireDucks is allowed to be missing."""
    result = []
    for name, module in ENGINE_MODULES.items():
        available = importlib.util.find_spec(module) is not None
        version = None
        if available:
            try:
                version = getattr(importlib.import_module(module), "__version__", None)
            except Exception:
                available = False
        result.append({"name": name, "available": available, "version": version})
    return result
