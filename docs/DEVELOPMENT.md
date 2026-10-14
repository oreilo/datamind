# Development

Install `python -m pip install -e ".[test]"`, then run `python -m pytest -q`.

Launch with `DATAMIND_API_KEY=your-secret datamind serve` (PowerShell: `$env:DATAMIND_API_KEY="your-secret"`). The original HTML dashboard remains available at `/`; advanced endpoints appear under `/api/docs`.

The `apps/web` React app is an additional frontend. From `apps/web`, run `npm install && npm run dev`. Configure `VITE_API_BASE` if your backend is not on `http://localhost:8000`.
