# Architecture

- `api.py`: authenticated REST API and bundled lightweight dashboard.
- `db.py`: SQLAlchemy metadata for dataset records and saved analyses.
- `ingest.py`: format-aware Pandas readers with row and column caps.
- `analytics.py`: deterministic statistics, correlation, grouping, outlier and anomaly detection, constrained natural-language interpretation.
- `charts.py`: Matplotlib PNG charts with bounded category counts.
- `reports.py`: PDF, Word, HTML, Markdown and JSON reports.
- `sdk.py`: synchronous HTTP client.
- `cli.py`: local file analysis and API server.

**Trust boundary:** the browser UI is untrusted; API key is required on all data endpoints. File parsing and CPU-intensive analysis currently run in-process. No arbitrary Python execution or generated SQL execution is exposed.
