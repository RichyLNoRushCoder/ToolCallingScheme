import pytest

from app.tools.builtins import anomaly_detector, data_quality_checker


@pytest.mark.asyncio
async def test_data_quality_checker_risk_high() -> None:
    payload = {"context": {"row_count": 100, "null_count": 30, "duplicate_count": 5}}
    result = await data_quality_checker(payload)
    assert result["risk_level"] == "high"
    assert result["null_rate"] == 0.3


@pytest.mark.asyncio
async def test_anomaly_detector_handles_short_series() -> None:
    payload = {"context": {"time_series": [1, 2]}}
    result = await anomaly_detector(payload)
    assert result["anomaly_points"] == []
    assert "insufficient" in result["note"]
