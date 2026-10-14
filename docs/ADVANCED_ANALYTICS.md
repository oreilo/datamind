# Advanced analytics

The v2 endpoints add deterministic regression, K-means clustering, isolation-forest anomaly detection, and simple linear-trend forecasting. These are exploratory tools, not automatic causal inference or guaranteed forecasts.

- `POST /api/v2/datasets/{id}/regression`: `{"features":["advertising"],"target":"sales"}`
- `POST /api/v2/datasets/{id}/clusters`: `{"columns":["sales","margin"],"count":3}`
- `POST /api/v2/datasets/{id}/anomalies`: `{"columns":["sales"],"contamination":0.05}`
- `POST /api/v2/datasets/{id}/forecast`: `{"date_column":"date","value_column":"sales","periods":6}`
- `POST /api/v2/datasets/{id}/transform`: `{"steps":[{"operation":"drop_duplicates"}]}`. Preview only; never overwrites uploaded data.
- `POST /api/v2/datasets/{id}/validate`: `{"rules":[{"type":"required","column":"sales"}]}`
- `POST /api/v2/datasets/{id}/visualization`: `{"kind":"bar","x":"region","y":"sales"}`

All endpoints require `X-API-Key`. Numerical outputs are computed locally from the dataset.
