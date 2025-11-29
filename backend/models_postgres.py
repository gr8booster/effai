"""
SQLAlchemy models for PostgreSQL - Financial and audit data
Production-ready schema with relationships and indexes
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text, JSON, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime, timezone
import os

Base = declarative_base()

# Database connection
DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER', 'postgres')}:{os.getenv('POSTGRES_PASSWORD', 'postgres')}@{os.getenv('POSTGRES_HOST', 'localhost')}:{os.getenv('POSTGRES_PORT', '5432')}/{os.getenv('POSTGRES_DB', 'eefsupport_pg')}"


class User(Base):
    """User accounts with authentication"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    role = Column(String(50), default="user", index=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    credit_reports = relationship("CreditReport", back_populates="user")
    financial_snapshots = relationship("FinancialSnapshot", back_populates="user")


class CreditReport(Base):
    """Credit report data - structured storage"""
    __tablename__ = "credit_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    bureau = Column(String(50), nullable=False)  # Equifax, Experian, TransUnion
    report_date = Column(DateTime(timezone=True), nullable=False)
    score = Column(Integer)
    accounts_data = Column(JSON)  # Full account details
    inquiries_data = Column(JSON)
    public_records_data = Column(JSON)
    uploaded_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    user = relationship("User", back_populates="credit_reports")
    
    __table_args__ = (Index('idx_user_bureau_date', 'user_id', 'bureau', 'report_date'),)


class FinancialSnapshot(Base):
    """Historical financial snapshots for tracking"""
    __tablename__ = "financial_snapshots"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    snapshot_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    income = Column(Float, nullable=False)
    expenses = Column(Float, nullable=False)
    savings = Column(Float, nullable=False)
    debts_total = Column(Float, default=0)
    credit_score_estimate = Column(Integer)
    monthly_surplus = Column(Float)
    
    user = relationship("User", back_populates="financial_snapshots")


class LegalTemplate(Base):
    """Versioned legal document templates"""
    __tablename__ = "legal_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(String(100), nullable=False, index=True)
    version = Column(String(20), nullable=False)
    template_type = Column(String(50), nullable=False)
    template_html = Column(Text, nullable=False)
    template_json = Column(JSON)
    legal_approved = Column(Boolean, default=False)
    approved_by = Column(String(255))
    approved_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    __table_args__ = (Index('idx_template_version', 'template_id', 'version', unique=True),)


class AuditLog(Base):
    """Immutable audit trail - PostgreSQL for compliance"""
    __tablename__ = "audit_log"
    
    id = Column(Integer, primary_key=True, index=True)
    provenance_id = Column(String(255), unique=True, nullable=False, index=True)
    agent_id = Column(String(100), nullable=False, index=True)
    agent_version = Column(String(50), nullable=False)
    input_hash = Column(String(255), nullable=False)
    output_hash = Column(String(255), nullable=False)
    s3_input_path = Column(String(500))
    s3_output_path = Column(String(500))
    db_refs = Column(JSON)
    legal_db_version = Column(String(50))
    cfp_version = Column(String(50))
    timestamp_utc = Column(DateTime(timezone=True), nullable=False, index=True)
    human_reviewed = Column(Boolean, default=False)
    hmac_signature = Column(String(500), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class LessonProgress(Base):
    """Track user lesson completion and scores"""
    __tablename__ = "lesson_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    lesson_id = Column(String(100), nullable=False, index=True)
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    quiz_score = Column(Integer)
    time_spent_seconds = Column(Integer)
    
    __table_args__ = (Index('idx_user_lesson', 'user_id', 'lesson_id'),)


def init_database():
    """Initialize PostgreSQL database with all tables"""
    engine = create_engine(DATABASE_URL, echo=False)
    Base.metadata.create_all(engine)
    return engine


def get_session():
    """Get database session"""
    engine = create_engine(DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()


if __name__ == "__main__":
    print("Initializing PostgreSQL schema...")
    try:
        engine = init_database()
        print("✅ PostgreSQL schema created successfully")
        print(f"   Tables: {list(Base.metadata.tables.keys())}")
    except Exception as e:
        print(f"❌ Failed: {e}")
