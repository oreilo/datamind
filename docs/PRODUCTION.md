# Production readiness checklist

This repository is a functional **developer baseline**, not a production-certified multi-tenant service.

Before any public deployment:

1. Verify all unit and API tests in your deployment environment.
2. Run end-to-end UI and file-upload tests with real datasets.
3. Put the API behind HTTPS with authentication, rate limiting and WAF protections.
4. Replace the single shared API key with organization/user identity and RBAC.
5. Add quotas for per-request CPU/memory, timeouts and background workers.
6. Isolate untrusted file parsers in hardened containers.
7. Configure encrypted backups, retention, deletion policies and disaster recovery.
8. Add structured audit logging, metrics and alerting.
9. Pin and scan dependencies and build signed release artifacts.
10. Perform security assessment, load tests, and recovery exercises.
11. Review privacy obligations for any personal or regulated data.
12. Add pagination and scalable storage for large data volumes.

Do not claim SOC2, ISO certification, guaranteed accuracy, or enterprise production readiness without independent evidence.
