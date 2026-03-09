# Enterprise Analysis Agent Architecture

## 1. Overall Flow

User -> API Gateway -> Agent Service -> (Planner + Tool Router + Tool Executor + Memory Manager) -> LLM -> External Tools

## 2. Key Components

- API Gateway (`app/gateway/api_gateway.py`)
  - Exposes `/v1/analyze`
  - Maps app exceptions to HTTP status
- Agent Service (`app/agents/orchestrator.py`)
  - Orchestrates plan, tool calls, and multi-agent execution
- Planner (`app/agents/planner.py`)
  - Produces execution plan steps
- Tool Registry/Router/Executor (`app/tools/*`)
  - Registry stores tool metadata and function pointers
  - Router selects tools based on intent
  - Executor adds timeout/retry and unified result record
- Memory Manager (`app/memory/manager.py`)
  - Short-term per-user request memory for context continuity
- LLM Client (`app/llm/deepseek_client.py`)
  - DeepSeek API wrapper with error mapping
- Multi-Agent
  - `AnalystAgent`: synthesize tool evidence into analysis
  - `QAAgent`: risk checks and guardrails before final output

## 3. Enterprise Design Choices

- Structured schema contracts (request/response/tool traces)
- Fault tolerance: timeout + retry + partial-result mode
- Agent traceability: each agent outputs explicit summary
- Extensibility: add tools by registration, add agents by planner and orchestrator
- Testability: unit + integration-like API tests with mocked LLM

## 4. Recommended Production Hardening

- Replace in-memory storage with Redis/Postgres memory backend
- Add authn/authz and tenant isolation in API gateway
- Add request-level observability (trace IDs, metrics, log aggregation)
- Add dynamic model fallback policy (DeepSeek primary, secondary provider backup)
- Add async task queue for long-running analyses
