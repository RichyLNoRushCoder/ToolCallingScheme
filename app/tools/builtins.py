from typing import Any


def _safe_series(payload: dict[str, Any]) -> list[float]:
    values = payload.get("context", {}).get("time_series", [])
    return [float(v) for v in values if isinstance(v, (int, float))]


async def data_quality_checker(payload: dict[str, Any]) -> dict[str, Any]:
    rows = int(payload.get("context", {}).get("row_count", 0))
    nulls = int(payload.get("context", {}).get("null_count", 0))
    dup = int(payload.get("context", {}).get("duplicate_count", 0))
    null_rate = 0.0 if rows == 0 else round(nulls / rows, 4)
    dup_rate = 0.0 if rows == 0 else round(dup / rows, 4)
    risk = "high" if null_rate > 0.2 or dup_rate > 0.1 else "medium" if null_rate > 0.05 else "low"
    return {
        "row_count": rows,
        "null_rate": null_rate,
        "duplicate_rate": dup_rate,
        "risk_level": risk,
    }


async def anomaly_detector(payload: dict[str, Any]) -> dict[str, Any]:
    series = _safe_series(payload)
    if len(series) < 3:
        return {"anomaly_points": [], "note": "insufficient time_series data"}

    mean = sum(series) / len(series)
    variance = sum((x - mean) ** 2 for x in series) / len(series)
    std = variance ** 0.5
    if std == 0:
        return {"anomaly_points": [], "note": "zero variance"}

    anomalies = [{"idx": idx, "value": val} for idx, val in enumerate(series) if abs((val - mean) / std) > 2.0]
    return {"anomaly_points": anomalies, "mean": round(mean, 4), "std": round(std, 4)}


async def report_generator(payload: dict[str, Any]) -> dict[str, Any]:
    summary = payload.get("context", {}).get("summary_hint", "No summary hint provided")
    return {
        "title": "Data Analysis Executive Summary",
        "sections": [
            "Data Quality",
            "Anomaly Detection",
            "Business Impact",
            "Action Items",
        ],
        "summary_hint": summary,
    }
