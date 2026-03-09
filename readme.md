# 企业级分析调用框架（多工具 + 多智能体 + DeepSeek）

该项目是一个可直接运行的企业级分析框架骨架，覆盖你给出的核心链路：

User -> API Gateway -> Agent Service -> Tool Registry/Router/Executor + Memory + Planner -> LLM(DeepSeek) -> External Tools

## 能力清单

- 多智能体协作
  - `AnalystAgent`: 综合工具结果生成业务分析
  - `QAAgent`: 风险审查与结论兜底
- 多工具调用
  - `ToolRegistry` 可插拔注册
  - `ToolRouter` 按意图选工具
  - `ToolExecutor` 统一超时/重试/失败记录
- 数据工作场景内置工具
  - 数据质量检查（空值/重复率）
  - 时序异常检测（z-score）
  - 管理层报告结构生成
- 企业级稳定性设计
  - 请求/响应与调用轨迹结构化
  - 错误分层、部分成功返回（`status=partial`）
  - 内存上下文管理（按用户保留最近请求）
- 完整测试样例
  - API 测试
  - 工具单元测试
  - 编排链路测试
  - LLM 异常分支测试

## 项目结构

```text
app/
  main.py
  gateway/api_gateway.py
  services/analysis_service.py
  agents/{planner.py,orchestrator.py,analyst_agent.py,qa_agent.py}
  tools/{registry.py,router.py,executor.py,builtins.py}
  memory/manager.py
  llm/deepseek_client.py
  core/config.py
  schemas.py
  utils/{errors.py,retry.py,logging.py}
tests/
docs/{architecture.md,runbook.md}
.env.example
```

## 快速启动

1. 创建环境并安装依赖

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env，填入 DEEPSEEK_API_KEY
```

3. 启动服务

```bash
uvicorn app.main:app --reload --port 8000
```

4. 调用接口

```bash
curl -X POST http://127.0.0.1:8000/v1/analyze \
  -H 'Content-Type: application/json' \
  -d '{
    "request_id": "req-001",
    "user_id": "u-001",
    "query": "请分析这批订单数据质量与异常波动并给出业务建议",
    "context": {
      "row_count": 12000,
      "null_count": 300,
      "duplicate_count": 100,
      "time_series": [120,130,128,400,129,127,126],
      "summary_hint": "核心订单量出现短期异常峰值"
    }
  }'
```

## 测试

```bash
pytest -q
```

## DeepSeek 接入说明

- 默认接口：`https://api.deepseek.com/chat/completions`
- 通过 `.env` 配置：
  - `DEEPSEEK_API_KEY`
  - `DEEPSEEK_BASE_URL`
  - `DEEPSEEK_MODEL`

未配置 Key 时会进入降级模式（返回 mock 文本），用于本地联调。

## 常见问题处理

见 [docs/runbook.md](docs/runbook.md)

## 下一步可扩展方向

- 引入 Redis/Postgres 持久化 Memory
- 增加 SQL 执行、元数据血缘、质量规则引擎等企业工具
- 增加并行计划执行与 DAG 调度
- 增加评估智能体与策略路由（模型切换、成本控制）
