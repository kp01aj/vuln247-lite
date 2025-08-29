from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .db import Base

class Finding(Base):
    __tablename__ = "findings"
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, nullable=False)
    target_id = Column(Integer, nullable=False)
    tool = Column(String, nullable=False)
    summary = Column(String, nullable=False)
    raw = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())