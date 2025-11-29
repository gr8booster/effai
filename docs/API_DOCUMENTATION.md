# EEFai Platform - Complete API Documentation

## Base URL
`https://eefsupport.preview.emergentagent.com/api`

---

## Authentication Endpoints

### POST /api/auth/register
Register new user account.

**Query Parameters:**
- `email` (string, required): User email
- `password` (string, required): Password (min 6 chars)
- `name` (string, required): Full name

**Response:**
```json
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer",
  "email": "user@example.com",
  "name": "User Name"
}
```

### POST /api/auth/login
Login existing user.

**Query Parameters:**
- `email` (string, required)
- `password` (string, required)

**Response:** Same as register

### GET /api/auth/me
Get current authenticated user.

**Headers:** `Authorization: Bearer {token}`

**Response:**
```json
{
  "email": "user@example.com",
  "name": "User Name",
  "role": "user",
  "active": true
}
```

---

## EEFai Agent Endpoints

### POST /api/eefai/create
Create EEFai instance for user.

**Request Body:**
```json
{
  "user_id": "user@example.com",
  "profile": {
    "income": 5000,
    "expenses": 3000,
    "savings": 1000,
    "debts": [],
    "goals": []
  }
}
```

### GET /api/eefai/{user_id}/state
Get user's EEFai state and profile.

**Response:**
```json
{
  "user_id": "user@example.com",
  "profile": {...},
  "conversation_history": [...],
  "current_plan_id": "plan_123",
  "stage": "stabilize"
}
```

### POST /api/eefai/{user_id}/message
Send message to EEFai.

**Request Body:**
```json
{
  "user_id": "user@example.com",
  "message": "I need help with debt",
  "trace_id": "trace_123"
}
```

**Response:**
```json
{
  "response_id": "resp_123",
  "text": "I can help you...",
  "actions": [{\"type\": \"task\", \"ref\": \"upload_document\"}]
}
```

---

## CFP-AI (Financial Planning) Endpoints

### POST /api/cfp/simulate
Calculate financial plan.

**Request Body:**
```json
{
  "user_id": "user@example.com",
  "scenario": {
    "balances": [{\"name\": \"Card\", \"balance\": 1000, \"apr\": 0.24}],
    "income": 3000,
    "expenses": 2200,
    "goal": {\"type\": \"emergency\", \"amount\": 1000, \"deadline_days\": 90}
  },
  "trace_id": "trace_123"
}
```

**Response:**
```json
{
  "ok": true,
  "calculations": {
    "monthly_surplus": 800,
    "savings_plan": [...],
    "paydown_schedule": [...]
  },
  "checksum": "abc123...",
  "assumptions": [...]
}
```

---

## Legal AI Endpoints

### POST /api/legal/check
Check legal compliance.

**Request Body:**
```json
{
  "action_type": "statute_check",
  "user_state": {\"state\": \"CA\"},
  "context": {\"debt_type\": \"credit_card\", \"account_date\": \"2018-01-01\"},
  "trace_id\": \"trace_123\"
}
```

**Response:**
```json
{
  "ok": true,
  "flags": [...],
  "citations": [...],
  "must_escalate": false
}
```

---

## Writer Agent Endpoints

### POST /api/writer/generate
Generate letter from template.

**Request Body:**
```json
{
  "template_id": "debt_validation_v1",
  "template_version": "1.0.0",
  "fields": {
    "date": "2025-11-29",
    "recipient_name": "ABC Collections",
    "account_number": "12345",
    "consumer_name": "John Doe",
    "consumer_address": "123 Main St"
  },
  "tone": "formal",
  "user_id": "user@example.com",
  "trace_id": "trace_123"
}
```

**Response:**
```json
{
  "html_preview": "<html>...</html>",
  "pdf_url": "/api/writer/download/{hash}",
  "hash": "abc123...",
  "provenance_ref": "writer_trace_123"
}
```

### GET /api/writer/download/{document_id}
Download generated PDF.

**Response:** PDF file download

### GET /api/writer/template/{template_id}
Get template metadata.

**Available Templates:**
- `debt_validation_v1`
- `cease_desist_v1`
- `credit_dispute_v1`
- `settlement_offer_v1`

---

## Credit Module Endpoints

### GET /api/credit/score/estimate
Estimate credit score.

**Query Parameters:**
- `user_id` (string, required)

**Response:**
```json
{
  "estimated_score": 720,
  "score_range": "Good",
  "factors": {...},
  "recommendations": [...]
}
```

### POST /api/credit/analyze
Analyze credit report data.

**Query Parameters:**
- `user_id` (string, required)

**Request Body:**
```json
{
  "current_score": 650,
  "accounts": [{...}]
}
```

**Response:**
```json
{
  "analysis_id": "analysis_123",
  "negative_items": [...],
  "recommendations": [...],
  "action_plan": [...]
}
```

---

## Mentor Agent Endpoints

### POST /api/mentor/generate-tasks
Generate daily tasks.

**Request Body:**
```json
{
  "user_id": "user@example.com",
  "plan_id": "plan_123",
  "milestone_id": "emergency_start",
  "trace_id": "trace_123"
}
```

### GET /api/mentor/lessons/list
Get all available lessons.

**Response:**
```json
{
  "lessons": [{\"id\": \"...\", \"title\": \"...\", \"category\": \"...\"}],
  "total": 70
}
```

### GET /api/mentor/lesson/{lesson_id}
Get specific lesson content.

### POST /api/mentor/tasks/{task_id}/complete
Mark task as completed.

**Query Parameters:**
- `user_id` (string, required)

### GET /api/mentor/tasks/active
Get active tasks for user.

**Query Parameters:**
- `user_id` (string, required)

---

## Support Agent Endpoints

### GET /api/support/queue
Get all items needing review.

### POST /api/support/review/{item_id}
Submit review decision.

**Request Body:**
```json
{
  "reviewer_id": "admin",
  "decision": "approve|reject|edit",
  "notes": "Review notes"
}
```

---

## Audit Agent Endpoints

### POST /api/audit/log
Log provenance record.

### GET /api/audit/{provenance_id}
Get provenance record.

### POST /api/audit/verify
Verify output hash.

### GET /api/audit/recent/{limit}
Get recent audit logs.

---

## Intake Agent Endpoints

### POST /api/intake/upload
Upload document for OCR processing.

**Form Data:**
- `file` (file, required): Document file
- `user_id` (string, required)
- `trace_id` (string, required)

**Response:**
```json
{
  "doc_id": "doc_123",
  "ocr_text": "extracted text...",
  "extracted_fields": {...},
  "redacted_preview": "...",
  "confidence_scores": {...},
  "needs_manual_review": false
}
```

---

## Response Format Standards

All successful responses include:
- HTTP 200 status
- JSON body
- `provenance_ref` for tracking (where applicable)

All error responses include:
- Appropriate HTTP status (400, 401, 404, 500)
- `{\"detail\": \"Error message\"}`

---

## Rate Limiting
- 60 requests per minute per IP
- 429 status code when exceeded
- Reset after 60 seconds

## Security Headers
- Strict-Transport-Security
- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff
- Content-Security-Policy
- X-XSS-Protection
