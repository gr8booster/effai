"""
Comprehensive Backend API Testing for EEFai Platform
Tests all 9 agents + Credit + Auth systems
"""
import requests
import sys
import json
from datetime import datetime

class EEFaiBackendTester:
    def __init__(self, base_url="https://eefsupport.preview.emergentagent.com"):
        self.base_url = base_url
        self.token = None
        self.test_user_email = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}@test.com"
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []
        self.passed_tests = []

    def log(self, message, level="INFO"):
        """Log test messages"""
        print(f"[{level}] {message}")

    def run_test(self, name, method, endpoint, expected_status, data=None, params=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'

        self.tests_run += 1
        self.log(f"\n🔍 Test {self.tests_run}: {name}")
        self.log(f"   Endpoint: {method} {endpoint}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, params=params, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, params=params, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, params=params, timeout=10)

            success = response.status_code == expected_status
            
            if success:
                self.tests_passed += 1
                self.passed_tests.append(name)
                self.log(f"✅ PASSED - Status: {response.status_code}", "SUCCESS")
                try:
                    response_data = response.json()
                    self.log(f"   Response: {json.dumps(response_data, indent=2)[:200]}...")
                except:
                    pass
            else:
                self.failed_tests.append({
                    "test": name,
                    "endpoint": endpoint,
                    "expected": expected_status,
                    "actual": response.status_code,
                    "response": response.text[:200]
                })
                self.log(f"❌ FAILED - Expected {expected_status}, got {response.status_code}", "ERROR")
                self.log(f"   Response: {response.text[:200]}", "ERROR")

            return success, response.json() if success and response.text else {}

        except requests.exceptions.Timeout:
            self.failed_tests.append({
                "test": name,
                "endpoint": endpoint,
                "error": "Request timeout (>10s)"
            })
            self.log(f"❌ FAILED - Request timeout", "ERROR")
            return False, {}
        except Exception as e:
            self.failed_tests.append({
                "test": name,
                "endpoint": endpoint,
                "error": str(e)
            })
            self.log(f"❌ FAILED - Error: {str(e)}", "ERROR")
            return False, {}

    # ========== HEALTH CHECK ==========
    def test_health_check(self):
        """Test API health endpoint"""
        success, response = self.run_test(
            "API Health Check",
            "GET",
            "api/",
            200
        )
        if success:
            assert "agents" in response, "Missing agents list in health check"
            assert len(response["agents"]) == 9, f"Expected 9 agents, got {len(response['agents'])}"
        return success

    # ========== AUTH TESTS ==========
    def test_register(self):
        """Test user registration"""
        success, response = self.run_test(
            "User Registration",
            "POST",
            "api/auth/register",
            200,
            params={
                "email": self.test_user_email,
                "password": "TestPass123!",
                "name": "Test User"
            }
        )
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.log(f"   Token obtained: {self.token[:20]}...", "INFO")
        return success

    def test_login(self):
        """Test user login"""
        success, response = self.run_test(
            "User Login",
            "POST",
            "api/auth/login",
            200,
            params={
                "email": self.test_user_email,
                "password": "TestPass123!"
            }
        )
        if success and 'access_token' in response:
            self.token = response['access_token']
        return success

    def test_get_current_user(self):
        """Test get current user endpoint"""
        success, response = self.run_test(
            "Get Current User",
            "GET",
            "api/auth/me",
            200
        )
        return success

    # ========== EEFAI TESTS ==========
    def test_create_eefai_instance(self):
        """Test EEFai instance creation"""
        success, response = self.run_test(
            "Create EEFai Instance",
            "POST",
            "api/eefai/create",
            200,
            data={
                "user_id": self.test_user_email,
                "profile": {
                    "income": 3000,
                    "expenses": 2200,
                    "savings": 500,
                    "debts": []
                }
            }
        )
        return success

    def test_get_eefai_state(self):
        """Test get EEFai state"""
        success, response = self.run_test(
            "Get EEFai State",
            "GET",
            f"api/eefai/{self.test_user_email}/state",
            200
        )
        if success:
            assert "profile" in response, "Missing profile in EEFai state"
            assert "conversation_history" in response, "Missing conversation_history"
        return success

    def test_send_message_to_eefai(self):
        """Test sending message to EEFai"""
        success, response = self.run_test(
            "Send Message to EEFai",
            "POST",
            f"api/eefai/{self.test_user_email}/message",
            200,
            data={
                "user_id": self.test_user_email,
                "message": "I need help with a debt collection letter",
                "trace_id": f"test_{datetime.now().timestamp()}"
            }
        )
        if success:
            assert "text" in response, "Missing response text"
            assert "actions" in response, "Missing actions"
        return success

    # ========== CFP-AI TESTS ==========
    def test_cfp_simulate(self):
        """Test CFP-AI financial simulation"""
        success, response = self.run_test(
            "CFP-AI Financial Simulation",
            "POST",
            "api/cfp/simulate",
            200,
            data={
                "user_id": self.test_user_email,
                "scenario": {
                    "balances": [],
                    "income": 3000,
                    "expenses": 2200,
                    "goal": {
                        "type": "emergency",
                        "amount": 1000,
                        "deadline_days": 90
                    }
                },
                "trace_id": f"test_cfp_{datetime.now().timestamp()}"
            }
        )
        if success:
            assert "calculations" in response, "Missing calculations"
            assert "monthly_surplus" in response["calculations"], "Missing monthly_surplus"
        return success

    # ========== LEGAL AI TESTS ==========
    def test_legal_check(self):
        """Test Legal AI check (not validate)"""
        success, response = self.run_test(
            "Legal AI Check",
            "POST",
            "api/legal/check",
            200,
            data={
                "action_type": "statute_check",
                "user_state": {"state": "CA"},
                "context": {
                    "debt_type": "credit_card",
                    "account_date": "2018-01-01"
                },
                "trace_id": f"test_legal_{datetime.now().timestamp()}"
            }
        )
        if success:
            assert "flags" in response, "Missing flags field"
            assert "citations" in response, "Missing citations field"
        return success

    # ========== WRITER AGENT TESTS ==========
    def test_writer_get_template(self):
        """Test get template metadata"""
        success, response = self.run_test(
            "Get Template Metadata",
            "GET",
            "api/writer/template/debt_validation_v1",
            200
        )
        if success:
            assert "template_id" in response, "Missing template_id"
            assert "required_fields" in response, "Missing required_fields"
        return success

    def test_writer_generate_debt_validation(self):
        """Test debt validation letter generation"""
        success, response = self.run_test(
            "Generate Debt Validation Letter",
            "POST",
            "api/writer/generate",
            200,
            data={
                "template_id": "debt_validation_v1",
                "template_version": "1.0.0",
                "fields": {
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "recipient_name": "ABC Collections",
                    "account_number": "123456789",
                    "consumer_name": "Test User",
                    "consumer_address": "123 Test St, Test City, CA 90001"
                },
                "tone": "formal",
                "user_id": self.test_user_email,
                "trace_id": f"test_writer_{datetime.now().timestamp()}"
            }
        )
        if success:
            assert "html_preview" in response, "Missing html_preview"
            assert "hash" in response, "Missing hash"
        return success

    def test_writer_generate_cease_desist(self):
        """Test cease and desist letter generation"""
        success, response = self.run_test(
            "Generate Cease & Desist Letter",
            "POST",
            "api/writer/generate",
            200,
            data={
                "template_id": "cease_desist_v1",
                "template_version": "1.0.0",
                "fields": {
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "recipient_name": "XYZ Debt Collectors",
                    "recipient_address": "456 Collector Ave, City, CA 90002",
                    "account_number": "987654321",
                    "consumer_name": "Test User",
                    "consumer_address": "123 Test St, Test City, CA 90001"
                },
                "tone": "formal",
                "user_id": self.test_user_email,
                "trace_id": f"test_cease_{datetime.now().timestamp()}"
            }
        )
        return success

    def test_writer_generate_credit_dispute(self):
        """Test credit dispute letter generation"""
        success, response = self.run_test(
            "Generate Credit Dispute Letter",
            "POST",
            "api/writer/generate",
            200,
            data={
                "template_id": "credit_dispute_v1",
                "template_version": "1.0.0",
                "fields": {
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "bureau_name": "Equifax",
                    "disputed_item": "Late payment on ABC Credit Card",
                    "account_number": "1234567890",
                    "dispute_reason": "This payment was made on time",
                    "consumer_name": "Test User",
                    "consumer_address": "123 Test St, Test City, CA 90001"
                },
                "tone": "formal",
                "user_id": self.test_user_email,
                "trace_id": f"test_dispute_{datetime.now().timestamp()}"
            }
        )
        return success

    def test_writer_generate_settlement(self):
        """Test settlement offer letter generation"""
        success, response = self.run_test(
            "Generate Settlement Offer Letter",
            "POST",
            "api/writer/generate",
            200,
            data={
                "template_id": "settlement_offer_v1",
                "template_version": "1.0.0",
                "fields": {
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "recipient_name": "ABC Collections",
                    "account_number": "123456789",
                    "settlement_amount": "500",
                    "settlement_percentage": "50",
                    "payment_method": "Certified check",
                    "consumer_name": "Test User",
                    "consumer_address": "123 Test St, Test City, CA 90001"
                },
                "tone": "formal",
                "user_id": self.test_user_email,
                "trace_id": f"test_settlement_{datetime.now().timestamp()}"
            }
        )
        return success

    # ========== CREDIT MODULE TESTS ==========
    def test_credit_score_estimate(self):
        """Test credit score estimation"""
        success, response = self.run_test(
            "Credit Score Estimation",
            "GET",
            f"api/credit/score/estimate",
            200,
            params={"user_id": self.test_user_email}
        )
        if success:
            assert "estimated_score" in response, "Missing estimated_score"
            assert "score_range" in response, "Missing score_range"
            assert "recommendations" in response, "Missing recommendations"
        return success

    def test_credit_analyze(self):
        """Test credit report analysis"""
        success, response = self.run_test(
            "Credit Report Analysis",
            "POST",
            "api/credit/analyze",
            200,
            params={"user_id": self.test_user_email},
            data={
                "current_score": 650,
                "accounts": [
                    {
                        "status": "collections",
                        "creditor": "ABC Bank",
                        "balance": 1500,
                        "date": "2023-01-01"
                    },
                    {
                        "type": "revolving",
                        "balance": 500,
                        "limit": 2000
                    }
                ]
            }
        )
        if success:
            assert "negative_items" in response, "Missing negative_items"
            assert "recommendations" in response, "Missing recommendations"
            assert "action_plan" in response, "Missing action_plan"
        return success

    # ========== MENTOR AGENT TESTS ==========
    def test_mentor_generate_tasks(self):
        """Test task generation"""
        success, response = self.run_test(
            "Generate Daily Tasks",
            "POST",
            "api/mentor/generate-tasks",
            200,
            data={
                "user_id": self.test_user_email,
                "plan_id": "test_plan",
                "milestone_id": "emergency_fund_start",
                "trace_id": f"test_mentor_{datetime.now().timestamp()}"
            }
        )
        if success:
            assert "tasks" in response, "Missing tasks"
        return success

    # ========== INTAKE AGENT TESTS ==========
    def test_intake_upload(self):
        """Test document upload (not extract)"""
        success, response = self.run_test(
            "Document Upload",
            "POST",
            "api/intake/upload",
            200,
            data={
                "document_text": "This is a debt collection letter from ABC Collections for account 123456789",
                "document_type": "debt_letter",
                "user_id": self.test_user_email,
                "trace_id": f"test_intake_{datetime.now().timestamp()}"
            }
        )
        if success:
            assert "doc_id" in response, "Missing doc_id"
        return success

    # ========== RUN ALL TESTS ==========
    def run_all_tests(self):
        """Run all backend tests"""
        self.log("\n" + "="*60)
        self.log("EEFAI PLATFORM BACKEND TESTING")
        self.log("="*60)
        
        # Health check
        self.log("\n--- HEALTH CHECK ---")
        self.test_health_check()
        
        # Auth tests
        self.log("\n--- AUTHENTICATION TESTS ---")
        self.test_register()
        self.test_login()
        self.test_get_current_user()
        
        # EEFai tests
        self.log("\n--- EEFAI AGENT TESTS ---")
        self.test_create_eefai_instance()
        self.test_get_eefai_state()
        self.test_send_message_to_eefai()
        
        # CFP-AI tests
        self.log("\n--- CFP-AI TESTS ---")
        self.test_cfp_simulate()
        
        # Legal AI tests
        self.log("\n--- LEGAL AI TESTS ---")
        self.test_legal_check()
        
        # Writer Agent tests (all 4 templates)
        self.log("\n--- WRITER AGENT TESTS (4 Templates) ---")
        self.test_writer_get_template()
        self.test_writer_generate_debt_validation()
        self.test_writer_generate_cease_desist()
        self.test_writer_generate_credit_dispute()
        self.test_writer_generate_settlement()
        
        # Credit module tests
        self.log("\n--- CREDIT MODULE TESTS ---")
        self.test_credit_score_estimate()
        self.test_credit_analyze()
        
        # Mentor Agent tests
        self.log("\n--- MENTOR AGENT TESTS ---")
        self.test_mentor_generate_tasks()
        
        # Intake Agent tests
        self.log("\n--- INTAKE AGENT TESTS ---")
        self.test_intake_upload()
        
        # Print summary
        self.print_summary()
        
        return self.tests_passed == self.tests_run

    def print_summary(self):
        """Print test summary"""
        self.log("\n" + "="*60)
        self.log("TEST SUMMARY")
        self.log("="*60)
        self.log(f"Total Tests: {self.tests_run}")
        self.log(f"Passed: {self.tests_passed} ✅")
        self.log(f"Failed: {len(self.failed_tests)} ❌")
        self.log(f"Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        
        if self.failed_tests:
            self.log("\n--- FAILED TESTS ---", "ERROR")
            for failure in self.failed_tests:
                self.log(f"❌ {failure['test']}", "ERROR")
                self.log(f"   Endpoint: {failure.get('endpoint', 'N/A')}", "ERROR")
                if 'expected' in failure:
                    self.log(f"   Expected: {failure['expected']}, Got: {failure['actual']}", "ERROR")
                if 'error' in failure:
                    self.log(f"   Error: {failure['error']}", "ERROR")
        
        self.log("\n" + "="*60)

def main():
    tester = EEFaiBackendTester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
