# EEFai Master Plan (One-and-Done)

This plan delivers the full EEFai platform in one cycle with a Core POC first, then full app build across 5 sprints. All API routes use the /api prefix. Static-first pages render without JS. Tri-database: MongoDB (user/EEFai state), PostgreSQL (legal templates, structured finance, audit), Redis (sessions, queues, short-term memory).

## 1) Objectives
- Prove core: OrchestratorAI → LegalAI/CFP-AI validation gate → AuditAgent provenance before any user-facing output.
- Implement 9 agents as FastAPI routers (microservices simulated via modules, ready to split later).
- Deterministic templates and finance math with checksums; human-in-loop for escalations.
- Static-first UI: Home, How It Works, Upload, Diagnosis, Plan, Letters, Coaching Dashboard.
- Full provenance (immutable logs) + state versioning; no hallucinations.
- AI: OpenAI GPT-4.1/4.1-mini (primary via Emergent LLM key), Claude Sonnet fallback.

## 2) Implementation Steps

### Phase 1 — POC (Core Orchestration & Validation) [Required]
Focus: Validate end-to-end pipeline deterministically.

1. Integration playbooks
   - Use integration_playbook_expert_v2 for: OpenAI (primary), Anthropic (fallback). Document model IDs, temperature=0 guards.
   - Decide OCR/PDF stack via web search: Tesseract + pdfkit/wkhtmltopdf/headless Chromium; pick env-compatible choice.
2. Data and schemas (deterministic)
   - Define canonical JSON for: orchestrator/run, legal/check, cfp/verify|simulate, writer/generate (dry-run), audit/log, support/review, intake/upload (stub w/ sample docs), eefai/message.
   - Add provenance schema (hashes, versions, timestamps, human_review flag).
3. Minimal tri-DB wiring
   - MongoDB: users, eefai_state, runs.
   - PostgreSQL: legal_templates, legal_rules, cfp_golden_vectors, audit_log.
   - Redis: job queue keys (run:{id}), rate limits.
4. Implement FastAPI routers (stubs with deterministic logic)
   - /api/orchestrator, /api/legal, /api/cfp, /api/writer, /api/intake, /api/mentor, /api/support, /api/audit, /api/eefai.
   - Gate: orchestrator requires ok:true from LegalAI and CFP-AI or routes to SupportAgent; always write to AuditAgent first.
5. Deterministic engines
   - LegalAI: rule-table driven checks (FDCPA/FCRA/CROA placeholders + SoL by state). No LLM for rules.
   - CFP-AI: pure math (Decimal) for surplus, amortization, snowball/avalanche, savings schedule, checksum.
   - WriterAgent: strict field whitelist; dry-run returns HTML + hash (no PDF yet in POC).
6. Security & PII in POC
   - Redact SSN/account; never log PII; return redacted_preview.
7. Test script (single Python): tests/test_core.py
   - Cover: orchestrator run → intake parse → legal.check & cfp.verify → audit.log written → support approval path → writer dry-run hash stable.
   - Repeat-run idempotency.
8. Fix-until-green, then snapshot artifacts
   - Save sprint1_provenance_sample.json, cfp_checks.json, pdf_hash.txt (dry-run), and POC report.

User Stories (Phase 1)
1. As a user, I can upload a sample debt letter and see redacted extracted fields.
2. As a user, my generated letter remains blocked until validation passes (visible status).
3. As an admin, I can retrieve a provenance record for a run and verify hashes.
4. As a planner, I can simulate a savings plan and receive a checksum to verify.
5. As a reviewer, I can approve a flagged item and resume the pipeline.
6. As a user, repeating the same action produces the same output hash.

Exit Criteria (POC)
- All core endpoints respond deterministically; test_core passes; provenance records persist; hashes stable; gate enforcement works.

### Phase 2 — Full App Development (All Features) via 5 Sprints
Build complete platform around proven core. Static-first UI, full CRUD, full validations, human-in-loop.

Sprint 1: Foundation & Orchestration
- Implement production-ready orchestrator with saga steps, retries, idempotency, feature flags.
- Complete AuditAgent (immutable logs + verify endpoint). Wire tri-DB migrations.
- Static pages: Home, How EEFai Works, Upload Document (no JS dependency).
- Deliverables: run-status UI (SSR), provenance viewer, service health endpoints.

Sprint 2: Onboarding & Diagnosis Engine
- EEFai instance per user (namespace in Mongo + vector-ready slots for future).
- Static onboarding form; diagnosis scoring (risk, SoL proximity, credit risk proxies, emergency buffer gap).
- Diagnosis PDF snapshot; daily baseline plan.
- Deliverables: /api/eefai state, /api/diagnosis, SSR Diagnosis Summary page.

Sprint 3: Defense Engine (Letters + Validation)
- IntakeAgent OCR + parsing + redaction; evidence tagging.
- WriterAgent: template store v1 (FDCPA debt validation, FCRA disputes, cease & desist, pay-for-delete, hardship); PDF rendering with embedded provenance JSON + SHA256.
- LegalAI full rule set (federal + state SoL table); SupportAgent reviewer console.
- Deliverables: Generate/download signed PDF; reviewer approve → orchestrator deliver.

Sprint 4: Financial Transformation Engine
- CFP-AI: amortization, snowball/avalanche, emergency fund builder, DTI/utilization models, savings micro-deposits generator.
- Savings tracker, debt payoff planner, emergency fund tracker UI (SSR + progressive enhance).
- MentorAgent: daily tasks + lessons (fixed template, temp=0 copy polish only) with provenance.

Sprint 5: Master Agent + Coaching Dashboard
- EEFai conversational routing (intent rules + temp=0 paraphrase), persistent memory, task nudges.
- Unified dashboard (letters, plans, lessons, savings progress).
- Notifications (in-app), streaks, and audit verify actions.

Shared Requirements (Phase 2)
- All legal/financial actions pass LegalAI + CFP-AI before exposure; escalations to Support.
- Templates: immutable, versioned; deterministic rendering; HMAC signing.
- Static HTML snapshots for all major pages for SEO/AEO.
- Accessibility, loading/error states, data-testid on interactive elements.

User Stories (Phase 2)
1. As a user, I can complete onboarding and receive a deterministic diagnosis PDF.
2. As a user, I can upload a collection letter, see parsed fields, and receive a validated dispute letter PDF.
3. As a user, I can create a savings goal and see a 90-day micro-deposit plan with checksum.
4. As a user, I can view a debt payoff schedule (snowball/avalanche) and export it.
5. As a user, I get a daily micro-lesson and can mark tasks done; streaks update.
6. As a reviewer, I can approve/reject/edit a flagged item; provenance updates immutably.
7. As a user, I can verify any PDF against stored audit hash via a Verify button.
8. As a user, all pages load without JS with full content visible.
9. As a user, re-running same inputs yields same letter hash.
10. As a user, I see clear validation messages if LegalAI/CFP-AI block an action.

Testing & Evidence (Phase 2)
- Use testing_agent_v3 for E2E: upload→diagnose→generate letter→approve→download PDF; savings & payoff flows; skip drag/drop/voice.
- Save sprint reports, screenshots, and verification artifacts.

## 3) Next Actions
1. Initiate integration playbook for OpenAI (primary) and Anthropic (fallback); retrieve EMERGENT_LLM_KEY via manager.
2. Implement Phase 1 routers and data schemas; wire tri-DB connections.
3. Write tests/test_core.py covering orchestration gate, provenance, CFP checksum, writer dry-run hash.
4. Run tests, fix until green; capture artifacts; then start Sprint 1 implementation.

## 4) Success Criteria
- POC: test_core passes; deterministic hashes; provenance persisted; gate enforcement verified.
- Phase 2: All user stories demonstrably pass; static-first pages render fully without JS; PDFs signed and verifiable; tri-DB operational.
- Validation: Every legal/financial action shows LegalAI/CFP-AI approval or Support escalation; no hallucinated content.
- Testing: testing_agent_v3 E2E report passes without critical issues; minor issues fixed.
