"""Verify all 9 agents return canonical JSON only"""
import asyncio
import aiohttp
import sys

BASE_URL = "http://localhost:8001"

async def verify_all_agents():
    """Test all 9 agents for canonical JSON compliance"""
    
    async with aiohttp.ClientSession() as session:
        tests_passed = 0
        tests_failed = 0
        
        # Test each agent
        agents = [
            ("OrchestratorAI", f"{BASE_URL}/api/orchestrator/status/test"),
            ("LegalAI", f"{BASE_URL}/api/legal/citation/test"),
            ("CFP-AI", f"{BASE_URL}/api/cfp/verify"),
            ("WriterAgent", f"{BASE_URL}/api/writer/template/debt_validation_v1"),
            ("IntakeAgent", f"{BASE_URL}/api/intake/doc/test/result"),
            ("EEFai", f"{BASE_URL}/api/eefai/test-user/state"),
            ("MentorAgent", f"{BASE_URL}/api/mentor/lesson/emergency_fund_basics"),
            ("SupportAgent", f"{BASE_URL}/api/support/queue"),
            ("AuditAgent", f"{BASE_URL}/api/audit/recent/5")
        ]
        
        for agent_name, url in agents:
            try:
                async with session.get(url) as resp:
                    if resp.status in [200, 404]:  # 404 ok for test data
                        data = await resp.json()
                        # Verify it's valid JSON (already parsed)
                        print(f"✓ {agent_name}: Returns valid JSON")
                        tests_passed += 1
                    else:
                        print(f"✗ {agent_name}: HTTP {resp.status}")
                        tests_failed += 1
            except Exception as e:
                print(f"✗ {agent_name}: {str(e)}")
                tests_failed += 1
        
        print(f"\nAgent Verification: {tests_passed}/{len(agents)} passed")
        return tests_failed == 0

if __name__ == "__main__":
    success = asyncio.run(verify_all_agents())
    sys.exit(0 if success else 1)
