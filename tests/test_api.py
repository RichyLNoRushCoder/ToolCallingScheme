def test_analyze_api(client) -> None:
    resp = client.post(
        "/v1/analyze",
        json={
            "request_id": "r-api-1",
            "user_id": "u-api",
            "query": "分析这份数据质量和异常情况并生成报告",
            "context": {
                "row_count": 200,
                "null_count": 10,
                "duplicate_count": 4,
                "time_series": [10, 12, 13, 50, 14, 13, 12],
                "summary_hint": "核心业务指标波动较大",
            },
        },
    )

    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] in ["ok", "partial"]
    assert data["request_id"] == "r-api-1"
    assert len(data["agent_traces"]) == 2
    assert len(data["tool_calls"]) >= 1
