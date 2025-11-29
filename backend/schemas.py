"""Canonical JSON schemas for all 9 agents"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    FAILED = "failed"
    COMPLETED = "completed"


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ToneType(str, Enum):
    FORMAL = "formal"
    PLAIN = "plain"


# ============ ORCHESTRATOR SCHEMAS ============

class OrchestratorRunInput(BaseModel):
    run_id: str = Field(description="Unique run identifier")
    user_id: str = Field(description="User identifier")
    action: str = Field(description="Action to perform, e.g., 'intake->diagnose->defend'")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Action-specific payload")
    trace_id: str = Field(description="Tracing identifier for debugging")


class AgentStepResult(BaseModel):
    agent: str
    status: str  # "ok" or "failed"
    output_ref: Optional[str] = None


class OrchestratorRunOutput(BaseModel):
    run_id: str
    status: TaskStatus
    steps: List[AgentStepResult] = Field(default_factory=list)
    provenance_ref: Optional[str] = None


# ============ LEGAL AI SCHEMAS ============

class UserState(BaseModel):
    state: str = Field(description="US state code, e.g., 'OH'")
    dob: Optional[str] = None
    account_date: Optional[str] = None


class LegalCheckInput(BaseModel):
    user_state: UserState
    action_type: str = Field(description="Type of action: debt_validation, settlement_offer, statute_check")
    context: Dict[str, Any] = Field(default_factory=dict)
    trace_id: str


class LegalFlag(BaseModel):
    code: str
    explanation: str
    severity: Severity
    citation_id: Optional[str] = None


class LegalCitation(BaseModel):
    id: str
    title: str
    text_snippet: str
    db_version: str


class LegalCheckOutput(BaseModel):
    ok: bool
    flags: List[LegalFlag] = Field(default_factory=list)
    citations: List[LegalCitation] = Field(default_factory=list)
    must_escalate: bool = False
    provenance_ref: Optional[str] = None


# ============ CFP-AI SCHEMAS ============

class BalanceInfo(BaseModel):
    name: str
    balance: float
    apr: float


class GoalInfo(BaseModel):
    type: str  # "emergency", "payoff", etc.
    amount: float
    deadline_days: int


class CFPScenario(BaseModel):
    balances: List[BalanceInfo] = Field(default_factory=list)
    income: float
    expenses: float
    goal: Optional[GoalInfo] = None


class CFPSimulateInput(BaseModel):
    user_id: str
    scenario: CFPScenario
    trace_id: str


class SavingsScheduleEntry(BaseModel):
    date: str
    amount: float


class PaydownScheduleEntry(BaseModel):
    account: str
    payment: float
    date: str


class CFPCalculations(BaseModel):
    monthly_surplus: float
    savings_plan: List[SavingsScheduleEntry] = Field(default_factory=list)
    paydown_schedule: List[PaydownScheduleEntry] = Field(default_factory=list)


class CFPSimulateOutput(BaseModel):
    ok: bool
    calculations: CFPCalculations
    checksum: str
    assumptions: List[str] = Field(default_factory=list)
    provenance_ref: Optional[str] = None


class CFPVerifyInput(BaseModel):
    calculations: Dict[str, Any]
    expected_checksum: str
    trace_id: str


class CFPVerifyOutput(BaseModel):
    ok: bool
    verified: bool
    message: str


# ============ WRITER AGENT SCHEMAS ============

class WriterGenerateInput(BaseModel):
    template_id: str
    template_version: str
    fields: Dict[str, Any]
    tone: ToneType = ToneType.FORMAL
    user_id: str
    trace_id: str


class WriterGenerateOutput(BaseModel):
    pdf_url: Optional[str] = None
    html_preview: Optional[str] = None  # For POC dry-run
    hash: str
    provenance_ref: Optional[str] = None


# ============ INTAKE AGENT SCHEMAS ============

class ExtractedField(BaseModel):
    value: Any
    confidence: float


class IntakeUploadOutput(BaseModel):
    doc_id: str
    ocr_text: str
    extracted_fields: Dict[str, ExtractedField] = Field(default_factory=dict)
    redacted_preview: str
    confidence_scores: Dict[str, float] = Field(default_factory=dict)
    needs_manual_review: bool
    provenance_ref: Optional[str] = None


# ============ EEFAI SCHEMAS ============

class EEFaiMessageInput(BaseModel):
    user_id: str
    message: str
    trace_id: str
    attachments: List[Dict[str, str]] = Field(default_factory=list)


class EEFaiAction(BaseModel):
    type: str  # "task", "letter", "plan"
    ref: str


class EEFaiMessageOutput(BaseModel):
    response_id: str
    text: str
    actions: List[EEFaiAction] = Field(default_factory=list)
    provenance_ref: Optional[str] = None


# ============ MENTOR AGENT SCHEMAS ============

class MentorTask(BaseModel):
    task_id: str
    description: str
    time_est_min: int
    resources: List[str] = Field(default_factory=list)
    provenance_ref: Optional[str] = None


class MentorLesson(BaseModel):
    id: str
    html: str


class MentorGenerateTasksInput(BaseModel):
    user_id: str
    plan_id: str
    milestone_id: str
    trace_id: str


class MentorGenerateTasksOutput(BaseModel):
    tasks: List[MentorTask]
    lesson_of_day: Optional[MentorLesson] = None


# ============ SUPPORT AGENT SCHEMAS ============

class SupportReviewDecision(str, Enum):
    APPROVE = "approve"
    REJECT = "reject"
    EDIT = "edit"


class SupportReviewInput(BaseModel):
    reviewer_id: str
    decision: SupportReviewDecision
    notes: str
    edited_payload: Optional[Dict[str, Any]] = None


class SupportReviewItem(BaseModel):
    item_id: str
    run_id: str
    agent_id: str
    payload: Dict[str, Any]
    provenance_ref: str
    flagged_reason: str
    created_at: datetime


# ============ AUDIT AGENT SCHEMAS ============

class AuditLogInput(BaseModel):
    provenance_id: str
    agent_id: str
    agent_version: str
    input_hash: str
    output_hash: str
    s3_input_path: Optional[str] = None
    s3_output_path: Optional[str] = None
    db_refs: Optional[Dict[str, Any]] = None
    legal_db_version: Optional[str] = None
    cfp_version: Optional[str] = None
    timestamp: datetime
    human_reviewed: bool = False


class AuditLogOutput(BaseModel):
    ok: bool
    provenance_id: str
    hmac_signature: str


class AuditVerifyInput(BaseModel):
    provenance_id: str
    output_hash: str


class AuditVerifyOutput(BaseModel):
    ok: bool
    verified: bool
    message: str
