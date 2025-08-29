from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from .db import Base

class Tenant(Base):
    __tablename__ = "tenants"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class Target(Base):
    __tablename__ = "targets"
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    value = Column(String, nullable=False)  # IP o FQDN
    created_at = Column(DateTime, server_default=func.now())

class Finding(Base):
    __tablename__ = "findings"
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, nullable=False)
    target_id = Column(Integer, nullable=False)
    tool = Column(String, nullable=False)
    summary = Column(String, nullable=False)
    raw = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())