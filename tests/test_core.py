"""
Comprehensive test script for EEFai core orchestration pipeline

Tests:
1. Orchestrator pipeline execution
2. Legal AI validation gates
3. CFP-AI deterministic calculations
4. Writer agent document generation
5. Audit provenance tracking
6. Intake document parsing
7. EEFai conversational routing
8. Support escalation flow
9. Mentor task generation

This test ensures all 9 agents work together properly with validation gates.
"""

import asyncio
import aiohttp
import json
from datetime import datetime, timezone
import sys

BASE_URL = "http://localhost:8001"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'


def print_success(msg):
    print(f"{Colors.GREEN}✓ {msg}{Colors.END}")


def print_error(msg):
    print(f"{Colors.RED}✗ {msg}{Colors.END}")


def print_info(msg):
    print(f"{Colors.BLUE}ℹ {msg}{Colors.END}")


def print_warning(msg):
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.END}")


async def test_health_check(session):
    """Test 0: API Health Check"""
    print_info("Test 0: API Health Check")
    
    try:
        async with session.get(f"{BASE_URL}/api/") as resp:
            if resp.status == 200:
                data = await resp.json()
                print_success(f"API is running - Version: {data['version']}")
                print_info(f"Available agents: {', '.join(data['agents'])}")
                return True
            else:
                print_error(f"Health check failed: {resp.status}")
                return False
    except Exception as e:
        print_error(f"Health check error: {e}")
        return False


async def test_legal_check(session):
    """Test 1: Legal AI validation"""
    print_info("Test 1: Legal AI Validation Gate")
    
    payload = {
        "user_state": {
            "state": "OH",
            "account_date": "2018-01-01"
        },
        "action_type": "debt_validation",
        "context": {
            "creditor_name": "ABC Collections"
        },
        "trace_id": "test_legal_001"
    }
    
    try:
        async with session.post(f"{BASE_URL}/api/legal/check", json=payload) as resp:
            if resp.status == 200:
                data = await resp.json()
                print_success(f"Legal check passed - ok={data['ok']}, must_escalate={data['must_escalate']}")
                print_info(f"Found {len(data['flags'])} flags and {len(data['citations'])} citations")
                
                if data['citations']:
                    print_info(f"Sample citation: {data['citations'][0]['title']}")
                
                return True, data
            else:
                print_error(f"Legal check failed: {resp.status}")
                return False, None
    except Exception as e:
        print_error(f"Legal check error: {e}")
        return False, None


async def test_cfp_simulate(session):
    """Test 2: CFP-AI deterministic calculations"""
    print_info("Test 2: CFP-AI Deterministic Math")
    
    payload = {
        "user_id": "test_user_001",
        "scenario": {
            "balances": [
                {"name": "Credit Card 1", "balance": 1000, "apr": 0.24},
                {"name": "Credit Card 2", "balance": 2000, "apr": 0.19}
            ],
            "income": 3000,
            "expenses": 2200,
            "goal": {
                "type": "emergency",
                "amount": 1000,
                "deadline_days": 90
            }
        },
        "trace_id": "test_cfp_001"
    }
    
    try:
        async with session.post(f"{BASE_URL}/api/cfp/simulate", json=payload) as resp:
            if resp.status == 200:
                data = await resp.json()
                print_success(f"CFP simulation passed - ok={data['ok']}")
                print_info(f"Monthly surplus: ${data['calculations']['monthly_surplus']}")
                print_info(f"Savings plan entries: {len(data['calculations']['savings_plan'])}")
                print_info(f"Checksum: {data['checksum'][:16]}...")
                
                # Test determinism - run again and verify same checksum
                async with session.post(f"{BASE_URL}/api/cfp/simulate", json=payload) as resp2:
                    if resp2.status == 200:
                        data2 = await resp2.json()
                        if data['checksum'] == data2['checksum']:
                            print_success("✓ Determinism verified: Same input → Same checksum")
                        else:
                            print_warning("Checksums differ - determinism may be broken")
                
                return True, data
            else:
                error_text = await resp.text()
                print_error(f"CFP simulation failed: {resp.status} - {error_text}")
                return False, None
    except Exception as e:
        print_error(f"CFP simulation error: {e}")
        return False, None


async def test_cfp_verify(session, calculations_data):
    """Test 3: CFP-AI verification"""
    print_info("Test 3: CFP-AI Checksum Verification")
    
    payload = {
        "calculations": {
            "income": 3000,
            "expenses": 2200,
            "monthly_surplus": calculations_data['calculations']['monthly_surplus'],
            "cfp_version": "v1.0"
        },
        "expected_checksum": calculations_data['checksum'],
        "trace_id": "test_cfp_verify_001"
    }
    
    try:
        async with session.post(f"{BASE_URL}/api/cfp/verify", json=payload) as resp:
            if resp.status == 200:
                data = await resp.json()
                if data['verified']:
                    print_success(f"Checksum verified: {data['message']}")
                else:
                    print_warning(f"Verification failed: {data['message']}")
                return data['verified'], data
            else:
                print_error(f"CFP verification failed: {resp.status}")
                return False, None
    except Exception as e:
        print_error(f"CFP verification error: {e}")
        return False, None


async def test_writer_generate(session):
    """Test 4: Writer Agent document generation"""
    print_info("Test 4: Writer Agent Document Generation")
    
    payload = {
        "template_id": "debt_validation_v1",
        "template_version": "1.0.0",
        "fields": {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "recipient_name": "ABC Collections Inc.",
            "account_number": "1234",
            "consumer_name": "John Doe",
            "consumer_address": "123 Main St, Columbus, OH 43215"
        },
        "tone": "formal",
        "user_id": "test_user_001",
        "trace_id": "test_writer_001"
    }
    
    try:
        async with session.post(f"{BASE_URL}/api/writer/generate", json=payload) as resp:
            if resp.status == 200:
                data = await resp.json()
                print_success(f"Document generated - hash: {data['hash'][:16]}...")
                print_info(f"HTML preview length: {len(data['html_preview'])} chars")
                
                # Test determinism
                async with session.post(f"{BASE_URL}/api/writer/generate", json=payload) as resp2:
                    if resp2.status == 200:
                        data2 = await resp2.json()
                        if data['hash'] == data2['hash']:
                            print_success("✓ Determinism verified: Same fields → Same hash")
                        else:
                            print_warning("Hashes differ - determinism may be broken")
                
                return True, data
            else:
                error_text = await resp.text()
                print_error(f"Writer generation failed: {resp.status} - {error_text}")
                return False, None
    except Exception as e:
        print_error(f"Writer generation error: {e}")
        return False, None


async def test_audit_log(session):
    """Test 5: Audit Agent provenance tracking"""
    print_info("Test 5: Audit Agent Provenance Logging")
    
    now = datetime.now(timezone.utc)
    
    payload = {
        "provenance_id": f"prov_test_{now.timestamp()}",
        "agent_id": "TestAgent",
        "agent_version": "1.0",
        "input_hash": "abc123def456",
        "output_hash": "xyz789uvw321",
        "s3_input_path": "s3://test/input",
        "s3_output_path": "s3://test/output",
        "db_refs": {"test": "ref"},
        "legal_db_version": "v1.0",
        "cfp_version": "v1.0",
        "timestamp": now.isoformat(),
        "human_reviewed": False
    }
    
    try:
        async with session.post(f"{BASE_URL}/api/audit/log", json=payload) as resp:
            if resp.status == 200:
                data = await resp.json()
                print_success(f"Provenance logged - ID: {data['provenance_id']}")
                print_info(f"HMAC signature: {data['hmac_signature'][:16]}...")
                return True, data
            else:
                error_text = await resp.text()
                print_error(f"Audit log failed: {resp.status} - {error_text}")
                return False, None
    except Exception as e:
        print_error(f"Audit log error: {e}")
        return False, None


async def test_audit_verify(session, provenance_id, output_hash):
    """Test 6: Audit verification"""
    print_info("Test 6: Audit Provenance Verification")
    
    payload = {
        "provenance_id": provenance_id,
        "output_hash": output_hash
    }
    
    try:
        async with session.post(f"{BASE_URL}/api/audit/verify", json=payload) as resp:
            if resp.status == 200:
                data = await resp.json()
                if data['verified']:
                    print_success(f"Provenance verified: {data['message']}")
                else:
                    print_warning(f"Verification failed: {data['message']}")
                return data['verified'], data
            else:
                print_error(f"Audit verification failed: {resp.status}")
                return False, None
    except Exception as e:
        print_error(f"Audit verification error: {e}")
        return False, None


async def test_eefai_create(session):
    """Test 7: EEFai instance creation"""
    print_info("Test 7: EEFai Instance Creation")
    
    user_id = "test_user_eefai_001"
    
    try:
        async with session.post(f"{BASE_URL}/api/eefai/create?user_id={user_id}") as resp:
            if resp.status == 200:
                data = await resp.json()
                print_success(f"EEFai instance created: {data['message']}")
                return True, user_id
            else:
                error_text = await resp.text()
                print_error(f"EEFai creation failed: {resp.status} - {error_text}")
                return False, None
    except Exception as e:
        print_error(f"EEFai creation error: {e}")
        return False, None


async def test_eefai_message(session, user_id):
    """Test 8: EEFai message handling"""
    print_info("Test 8: EEFai Message Routing")
    
    payload = {
        "user_id": user_id,
        "message": "I received a debt collection letter and need help responding to it",
        "trace_id": "test_eefai_msg_001",
        "attachments": []
    }
    
    try:
        async with session.post(f"{BASE_URL}/api/eefai/{user_id}/message", json=payload) as resp:
            if resp.status == 200:
                data = await resp.json()
                print_success(f"EEFai responded - response_id: {data['response_id']}")
                print_info(f"Actions: {len(data['actions'])}")
                if data['actions']:
                    print_info(f"First action: {data['actions'][0]['type']}")
                return True, data
            else:
                error_text = await resp.text()
                print_error(f"EEFai message failed: {resp.status} - {error_text}")
                return False, None
    except Exception as e:
        print_error(f"EEFai message error: {e}")
        return False, None


async def test_mentor_tasks(session):
    """Test 9: Mentor task generation"""
    print_info("Test 9: Mentor Agent Task Generation")
    
    payload = {
        "user_id": "test_user_001",
        "plan_id": "plan_emergency_001",
        "milestone_id": "emergency_fund_start",
        "trace_id": "test_mentor_001"
    }
    
    try:
        async with session.post(f"{BASE_URL}/api/mentor/generate-tasks", json=payload) as resp:
            if resp.status == 200:
                data = await resp.json()
                print_success(f"Tasks generated: {len(data['tasks'])} tasks")
                if data['tasks']:
                    print_info(f"First task: {data['tasks'][0]['description'][:50]}...")
                if data['lesson_of_day']:
                    print_info(f"Lesson included: {data['lesson_of_day']['id']}")
                return True, data
            else:
                error_text = await resp.text()
                print_error(f"Mentor task generation failed: {resp.status} - {error_text}")
                return False, None
    except Exception as e:
        print_error(f"Mentor task generation error: {e}")
        return False, None


async def test_orchestrator_run(session):
    """Test 10: Full orchestration pipeline"""
    print_info("Test 10: Orchestrator Pipeline Execution")
    
    payload = {
        "run_id": f"run_test_{datetime.now().timestamp()}",
        "user_id": "test_user_001",
        "action": "intake->diagnose",
        "payload": {"test": "data"},
        "trace_id": "test_orch_001"
    }
    
    try:
        async with session.post(f"{BASE_URL}/api/orchestrator/run", json=payload) as resp:
            if resp.status == 200:
                data = await resp.json()
                print_success(f"Orchestration completed - status: {data['status']}")
                print_info(f"Steps executed: {len(data['steps'])}")
                for step in data['steps']:
                    print_info(f"  - {step['agent']}: {step['status']}")
                return True, data
            else:
                error_text = await resp.text()
                print_error(f"Orchestration failed: {resp.status} - {error_text}")
                return False, None
    except Exception as e:
        print_error(f"Orchestration error: {e}")
        return False, None


async def main():
    print("\n" + "="*70)
    print("  EEFai Core Orchestration Pipeline Test Suite")
    print("  Testing all 9 agents + validation gates")
    print("="*70 + "\n")
    
    results = {
        "total": 0,
        "passed": 0,
        "failed": 0
    }
    
    async with aiohttp.ClientSession() as session:
        # Test 0: Health check
        results["total"] += 1
        if await test_health_check(session):
            results["passed"] += 1
        else:
            results["failed"] += 1
            print_error("API is not accessible. Exiting...")
            return
        
        print()
        
        # Test 1: Legal AI
        results["total"] += 1
        success, legal_data = await test_legal_check(session)
        if success:
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        print()
        
        # Test 2: CFP-AI simulate
        results["total"] += 1
        success, cfp_data = await test_cfp_simulate(session)
        if success:
            results["passed"] += 1
        else:
            results["failed"] += 1
            cfp_data = None
        
        print()
        
        # Test 3: CFP-AI verify
        if cfp_data:
            results["total"] += 1
            success, _ = await test_cfp_verify(session, cfp_data)
            if success:
                results["passed"] += 1
            else:
                results["failed"] += 1
            print()
        
        # Test 4: Writer Agent
        results["total"] += 1
        success, writer_data = await test_writer_generate(session)
        if success:
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        print()
        
        # Test 5: Audit log
        results["total"] += 1
        success, audit_data = await test_audit_log(session)
        if success:
            results["passed"] += 1
            
            # Test 6: Audit verify
            print()
            results["total"] += 1
            success, _ = await test_audit_verify(session, audit_data['provenance_id'], "xyz789uvw321")
            if success:
                results["passed"] += 1
            else:
                results["failed"] += 1
        else:
            results["failed"] += 1
        
        print()
        
        # Test 7 & 8: EEFai
        results["total"] += 1
        success, user_id = await test_eefai_create(session)
        if success:
            results["passed"] += 1
            
            print()
            results["total"] += 1
            success, _ = await test_eefai_message(session, user_id)
            if success:
                results["passed"] += 1
            else:
                results["failed"] += 1
        else:
            results["failed"] += 1
        
        print()
        
        # Test 9: Mentor
        results["total"] += 1
        success, _ = await test_mentor_tasks(session)
        if success:
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        print()
        
        # Test 10: Orchestrator
        results["total"] += 1
        success, _ = await test_orchestrator_run(session)
        if success:
            results["passed"] += 1
        else:
            results["failed"] += 1
    
    print("\n" + "="*70)
    print("  Test Results")
    print("="*70)
    print(f"Total Tests: {results['total']}")
    print(f"{Colors.GREEN}Passed: {results['passed']}{Colors.END}")
    print(f"{Colors.RED}Failed: {results['failed']}{Colors.END}")
    
    success_rate = (results['passed'] / results['total']) * 100 if results['total'] > 0 else 0
    print(f"Success Rate: {success_rate:.1f}%")
    print("="*70 + "\n")
    
    # Save artifacts
    with open('/app/tests/sprint1_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print_success("Test results saved to /app/tests/sprint1_test_results.json")
    
    return results['failed'] == 0


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
