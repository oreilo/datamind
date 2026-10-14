# AI analysis team

This optional workflow uses an OpenAI-compatible chat-completions endpoint to create a constrained analysis plan. The model does **not** run arbitrary Python or SQL. Allowed operations are checked against an explicit allowlist, then executed by the local deterministic analytics engine. A verification event records that numerical results came from tools.

Set `DATAMIND_LLM_BASE_URL` (including `/v1`), `DATAMIND_LLM_MODEL`, and `DATAMIND_LLM_API_KEY`. Use `POST /api/v2/datasets/{id}/agent-analysis` with `{"question":"Summarize this dataset"}`.

This is an orchestrated planner/analyst/verifier pipeline, not a fully independent seven-agent team. LLM interpretations may be wrong. Data is sent to the configured model only as column names and the question during planning.
