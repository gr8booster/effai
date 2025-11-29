# EEFai Platform - Production Deployment Runbook

## Pre-Deployment Checklist

### 1. Environment Setup
- [ ] MongoDB connection string configured
- [ ] PostgreSQL connection established
- [ ] Redis cache operational
- [ ] Emergent LLM Key loaded
- [ ] S3 bucket created (for file storage)
- [ ] KMS keys configured (for production HMAC)

### 2. Database Migrations
```bash
# Run PostgreSQL schema initialization
cd /app/backend
python -c "import asyncio; from database import init_databases; asyncio.run(init_databases())"

# Seed legal data
python seed_data.py
```

### 3. Security Configuration
- [ ] CORS origins restricted (update `.env`)
- [ ] Rate limiting enabled (Redis)
- [ ] CSRF protection activated
- [ ] Security headers configured
- [ ] PII encryption keys rotated

### 4. Test Verification
```bash
# Run full test suite
cd /app
python tests/test_core.py

# Expected: 10/11 tests passing (90.9%)
```

### 5. Static Rendering Verification
```bash
# Test no-JS rendering
curl -L https://eefsupport.preview.emergentagent.com/onboarding | grep "EEFai"

# Expected: HTML content with form visible
```

---

## Deployment Steps

### Staging Deployment

```bash
# 1. Build frontend
cd /app/frontend
yarn build

# 2. Restart services
supervisorctl restart backend frontend

# 3. Verify health
curl https://eefsupport.preview.emergentagent.com/api/
# Expected: {"message":"EEFai Platform API","version":"1.0.0","status":"running"}

# 4. Test key flows
curl -X POST https://eefsupport.preview.emergentagent.com/api/eefai/create?user_id=test_user
```

### Production Deployment (Canary Strategy)

**Phase 1: Canary (5% traffic)**
```bash
# Deploy to production cluster
kubectl apply -f infra/k8s/canary-deploy.yaml

# Monitor KPIs for 24-72 hours:
# - Error rate < 0.1%
# - P95 latency < 3s
# - Test pass rate maintained
```

**Phase 2: Full Rollout**
```bash
# If canary metrics green
kubectl apply -f infra/k8s/production-deploy.yaml

# Full traffic cutover
kubectl patch deployment eefai-frontend -p '{"spec":{"replicas":3}}'
kubectl patch deployment eefai-backend -p '{"spec":{"replicas":5}}'
```

---

## Rollback Procedure

### Emergency Rollback
```bash
# 1. Revert to previous deployment
kubectl rollout undo deployment/eefai-backend
kubectl rollout undo deployment/eefai-frontend

# 2. Restore database snapshot (if schema changed)
psql -h $POSTGRES_HOST -U postgres -d eefsupport_pg < backups/pre_deploy_snapshot.sql

# 3. Clear Redis cache
redis-cli FLUSHDB

# 4. Verify rollback
curl https://eefsupport.preview.emergentagent.com/api/
```

---

## Monitoring & Alerts

### Key Metrics to Monitor

**Application Health:**
- Service uptime (target: 99.9%)
- API response time (P95 < 3s)
- Error rate (< 0.1%)

**AI Agents:**
- LegalAI validation pass rate
- CFP-AI calculation accuracy  
- Orchestrator pipeline success rate
- AuditAgent provenance logging rate

**Database:**
- MongoDB connection pool utilization
- PostgreSQL query latency
- Redis cache hit rate

**User Engagement:**
- Onboarding completion rate
- Daily active users
- Letter generation count
- Task completion rate

### Alert Thresholds

**Critical Alerts:**
- API error rate > 1%
- Database connection failures
- Audit hash verification failures
- LegalAI must_escalate spike (>10%)

**Warning Alerts:**
- API latency P95 > 5s
- Redis memory > 80%
- PostgreSQL connections > 80%

---

## Configuration Management

### Environment Variables (.env)

**Backend:**
```bash
MONGO_URL="mongodb://localhost:27017"
DB_NAME="eefsupport_db"
POSTGRES_HOST="localhost"
POSTGRES_PORT="5432"
POSTGRES_USER="postgres"
POSTGRES_PASSWORD="<secure_password>"
POSTGRES_DB="eefsupport_pg"
REDIS_HOST="localhost"
REDIS_PORT="6379"
REDIS_DB="0"
EMERGENT_LLM_KEY="<emergent_key>"
CORS_ORIGINS="https://eefsupport.emergentagent.com"
```

**Frontend:**
```bash
REACT_APP_BACKEND_URL="<backend_url>"
```

---

## Security Hardening

### Pre-Production Security Checklist

- [ ] Run SAST scan (Snyk/SonarQube)
- [ ] Run DAST scan (OWASP ZAP)
- [ ] Penetration testing completed
- [ ] PII encryption verified
- [ ] HMAC key rotation tested
- [ ] Rate limiting functional
- [ ] CSRF protection enabled
- [ ] SQL injection prevention verified
- [ ] XSS prevention verified
- [ ] Audit logs immutable

---

## Human Sign-Off Requirements

### Legal Team
- [ ] Review all letter templates
- [ ] Verify FDCPA/FCRA/CROA compliance
- [ ] Approve disclaimers and consent language
- [ ] Sign off on legal DB versioning

### CFP Team
- [ ] Validate calculation engine
- [ ] Review financial assumptions
- [ ] Approve golden vector tests
- [ ] Sign off on checksum methodology

### Product Team
- [ ] Feature completeness verified
- [ ] User flows tested
- [ ] Documentation reviewed
- [ ] Beta user feedback incorporated

---

## Emergency Contacts

**On-Call Escalation:**
- P1 (Critical): Platform down, data breach
- P2 (High): Agent failures, validation gate issues
- P3 (Medium): Performance degradation
- P4 (Low): Minor bugs, UX issues

---

## Maintenance Schedule

**Daily:**
- Verify audit chain integrity
- Check error logs
- Monitor user signups

**Weekly:**
- Database backups
- Performance review
- Security patch updates

**Monthly:**
- HMAC key rotation
- Legal DB updates (as needed)
- Load testing

**Quarterly:**
- Disaster recovery drill
- Security audit
- Compliance review

---

**Document Version:** 1.0  
**Last Updated:** 2025-11-29  
**Owner:** EEFai Platform Team
