# OREiLO DataMind v2.0

**Open-source analytics workbench with a React dashboard, Python API, deterministic statistics, optional AI-guided analysis, data quality tools, and exportable reports.**

> **Release classification: expanded development release, not production-certified.** This is a substantial expansion of v1.0 with functional subsystems, but not a finished enterprise multi-tenant analytics SaaS. Read [security and limitations](docs/SECURITY_LIMITATIONS.md) before deployment.

## Features

- Import CSV, Excel, JSON, and Parquet; preview and profile data.
- Analyze datasets using summary statistics, correlations, missing-value analysis, and outlier inspection.
- Perform linear regression, K-means segmentation, Isolation Forest anomaly detection, and basic trend projection.
- Preview non-destructive cleaning transformations and enforce configurable data validation rules.
- Generate Vega-Lite visualization specifications and downloadable reports (PDF, DOCX, HTML, Markdown, JSON).
- Use an optional OpenAI-compatible model to plan a constrained series of **real, deterministic** analytics operations. No arbitrary AI-generated code execution.
- Manage projects and saved analysis questions in a local SQLite workspace.
- Query supported SQLAlchemy databases using a limited read-only SELECT helper (see security warning).
- Use REST API, Python SDK, CLI, classic built-in dashboard, or standalone React dashboard.
- Local audit, redaction, webhook signing, and in-process job primitives.

## Install

```bash
python -m pip install -e ".[test]"
python -m pytest -q
```

Set an API key and run:

```bash
export DATAMIND_API_KEY='replace-with-a-long-random-secret'
datamind serve
```

PowerShell:

```powershell
$env:DATAMIND_API_KEY = 'replace-with-a-long-random-secret'
datamind serve
```

Open `http://127.0.0.1:8000` for the built-in dashboard or `http://127.0.0.1:8000/api/docs` for interactive API documentation.

## React dashboard

```bash
cd apps/web
npm install
npm run dev
```

Open `http://127.0.0.1:5173`. Vite proxies API requests to the local backend. The dashboard includes overview, dataset library, AI analyst, chart studio, quality preview, and report downloads. Advanced statistical features are available through the API.

## AI setup (optional)

```bash
export DATAMIND_LLM_BASE_URL='https://YOUR-PROVIDER/v1'
export DATAMIND_LLM_MODEL='YOUR-MODEL'
export DATAMIND_LLM_API_KEY='YOUR-KEY'
```

The model receives the user's question and dataset column names for planning; actual numeric calculations happen locally. See [AI agent guide](docs/AI_AGENTS.md).

## Advanced API

Endpoints live at `/api/v2` and require `X-API-Key`. See [advanced analytics guide](docs/ADVANCED_ANALYTICS.md). Existing `/api` endpoints remain supported.

## Repository layout

- `src/datamind/` - API, analytics, ingestion, reporting, agents, SQL connectors, cleaning, validation, governance, jobs, and workspace.
- `apps/web/` - React + TypeScript dashboard.
- `tests/` - deterministic regression tests.
- `docs/` - deployment, security, architecture, API, and development notes.
- `samples/` - example sales dataset.

## Known limitations

No SSO, RBAC, tenant isolation, durable distributed queue, secure general-purpose Python sandbox, or validated production deployment. A single shared API key protects the API. The SQL query guard is **not** a substitute for database-enforced read-only privileges. Forecasting uses simple trend extrapolation and should not be presented as reliable predictions. React dashboard compilation and real browser interactions require separate validation in a Node/browser environment.

## License

MIT. Copyright (c) 2026 OREiLO.
