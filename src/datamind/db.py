from datetime import datetime, timezone
from sqlalchemy import create_engine, Column, String, DateTime, Integer, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from .config import DB_URL
engine = create_engine(DB_URL, connect_args={"check_same_thread": False} if DB_URL.startswith("sqlite") else {}, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
def now(): return datetime.now(timezone.utc)
class Dataset(Base):
    __tablename__ = "datasets"
    id = Column(String(36), primary_key=True)
    name = Column(String(200), nullable=False)
    filename = Column(String(255), nullable=False)
    path = Column(Text, nullable=False)
    rows = Column(Integer, nullable=False)
    columns = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=now)
class Analysis(Base):
    __tablename__ = "analyses"
    id = Column(String(36), primary_key=True)
    dataset_id = Column(String(36), ForeignKey("datasets.id"), nullable=False)
    question = Column(Text, nullable=False)
    result = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=now)
def init_db(): Base.metadata.create_all(engine)
