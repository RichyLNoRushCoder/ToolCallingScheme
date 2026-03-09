# Common Issues and Handling Playbook

## 1. DeepSeek API timeout
- Symptoms: `deepseek request timeout`
- Actions:
  - Increase `LLM_TIMEOUT_SECONDS`
  - Check network egress and API endpoint reachability
  - Enable model fallback strategy

## 2. HTTP 401/403 from DeepSeek
- Symptoms: `deepseek http error: 401/403`
- Actions:
  - Verify `DEEPSEEK_API_KEY`
  - Confirm key scope and project binding
  - Rotate key if leaked

## 3. Tool execution timeout
- Symptoms: `tool_failed:*:timeout`
- Actions:
  - Increase `TOOL_TIMEOUT_SECONDS`
  - Profile slow tools and split heavy tasks
  - Move heavy tool calls to async queue

## 4. Partial result returned
- Symptoms: response `status=partial`
- Actions:
  - Inspect `warnings` and failed tool traces
  - Retry failed tools or apply cached historical results

## 5. Empty/weak final answer
- Symptoms: output missing business conclusions
- Actions:
  - Improve prompt templates and planner decomposition
  - Add domain-specific tools (SQL lineage, KPI diagnostics, forecast)
  - Add evaluator agent for quality scoring

## 6. Memory pollution
- Symptoms: old context affects current analysis
- Actions:
  - Lower `MAX_MEMORY_ITEMS`
  - Add memory TTL and session boundaries
  - Add context relevance filtering
