# Security and production limitations

**Not production certified.** The included API uses a single shared API key; there is no tenant isolation, RBAC, SSO, audit retention policy, or independent penetration test. Do not expose it directly to the public internet. Place behind TLS, authentication, network restrictions, and a reverse proxy. Use a dedicated database read-only account for SQL connectors.

The SQL validator is defense in depth, not a SQL sandbox. It accepts only a single SELECT and blocks common mutation keywords, but database-specific functions may still have side effects. Never connect a privileged database account. Prefer a read-only replica with statement timeouts and row limits.

LLM planning is optional and constrained to preapproved deterministic analytics operations. Model output must not be treated as trusted instructions. Webhook destinations are allowlisted, but no network dispatcher is included.

The local job runner is in-process, not durable across restarts. No claim of distributed workers or enterprise scheduling is made.
