import os
from pathlib import Path
DATA_DIR = Path(os.getenv("DATAMIND_DATA_DIR", "./data")).resolve()
DATA_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_DIR = DATA_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)
DB_URL = os.getenv("DATAMIND_DATABASE_URL", f"sqlite:///{DATA_DIR / 'datamind.db'}")
API_KEY = os.getenv("DATAMIND_API_KEY", "")
MAX_UPLOAD_MB = int(os.getenv("DATAMIND_MAX_UPLOAD_MB", "25"))
MAX_ROWS = int(os.getenv("DATAMIND_MAX_ROWS", "250000"))
ALLOWED_ORIGINS = [s.strip() for s in os.getenv("DATAMIND_CORS_ORIGINS", "").split(",") if s.strip()]
