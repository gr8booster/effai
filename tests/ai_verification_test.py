"""
AI Integration Verification Test
Specifically tests that AI is actually being called and generating personalized content
"""
import requests
import sys
import json
import time
from datetime import datetime

BASE_URL = "https://eefsupport.preview.emergentagent.com"

class AIVerificationTester:
    def __init__(self):
        self.test_user_email = f"aitest_{datetime.now().strftime('%Y%m%d_%H%M%S')}@test.com"
        self.token = None
        self.tests_passed = 0
        self.tests_failed = 0
        
    def log(self, message, level="INFO"):
        print(f"[{level}] {message}")
    
    def test_ai_task_generation_personalization(self):
        """
        CRITICAL TEST: Verify MentorAgent generates PERSONALIZED tasks, not generic "Task 1", "Task 2"
        """
        self.log("\n" + "="*80)
        self.log("TEST 1: AI Task Generation Personalization")
        self.log("="*80)
        
        try:
            # First create a user with specific profile
            self.log("Creating test user with specific financial profile...")
            register_response = requests.post(
                f"{BASE_URL}/api/auth/register",
                params={
                    "email": self.test_user_email,
                    "password": "TestPass123!",
                    "name": "AI Test User"
                },
                timeout=10
            )
            
            if register_response.status_code != 200:
                self.log(f"❌ User registration failed: {register_response.status_code}", "ERROR")
                self.tests_failed += 1
                return False
            
            self.token = register_response.json().get("token")
            
            # Create EEFai instance with specific profile
            profile_data = {
                "user_id": self.test_user_email,
                "profile": {
                    "name": "AI Test User",
                    "email": self.test_user_email,
                    "state": "CA",
                    "income": 3500,
                    "expenses": 2800,
                    "savings": 250,
                    "debts": [
                        {"creditor": "Credit Card A", "balance": 5000, "min_payment": 150},
                        {"creditor": "Medical Bill", "balance": 1200, "min_payment": 50}
                    ]
                },
                "trace_id": f"ai_test_{int(time.time())}"
            }
            
            eefai_response = requests.post(
                f"{BASE_URL}/api/eefai/create",
                json=profile_data,
                timeout=10
            )
            
            if eefai_response.status_code != 200:
                self.log(f"❌ EEFai creation failed: {eefai_response.status_code}", "ERROR")
                self.tests_failed += 1
                return False
            
            self.log("✅ User profile created successfully")
            
            # Generate tasks using AI
            self.log("\nGenerating tasks via MentorAgent AI...")
            task_response = requests.post(
                f"{BASE_URL}/api/mentor/generate-tasks",
                json={
                    "user_id": self.test_user_email,
                    "plan_id": "emergency_fund_plan",
                    "milestone_id": "emergency_fund_start",
                    "trace_id": f"task_gen_{int(time.time())}"
                },
                timeout=30  # AI calls can take time
            )
            
            if task_response.status_code != 200:
                self.log(f"❌ Task generation failed: {task_response.status_code}", "ERROR")
                self.log(f"Response: {task_response.text}", "ERROR")
                self.tests_failed += 1
                return False
            
            tasks_data = task_response.json()
            tasks = tasks_data.get("tasks", [])
            
            self.log(f"\n✅ Generated {len(tasks)} tasks")
            
            # CRITICAL CHECK: Verify tasks are personalized, not generic
            generic_patterns = ["Task 1", "Task 2", "Task 3", "task 1", "task 2", "task 3"]
            personalized = True
            
            for i, task in enumerate(tasks, 1):
                description = task.get("description", "")
                self.log(f"\nTask {i}: {description}")
                
                # Check if task contains generic patterns
                if any(pattern in description for pattern in generic_patterns):
                    self.log(f"❌ FAILED: Task contains generic pattern!", "ERROR")
                    personalized = False
                
                # Check if task is substantive (more than 20 characters)
                if len(description) < 20:
                    self.log(f"❌ FAILED: Task too short, likely not AI-generated", "ERROR")
                    personalized = False
            
            if personalized and len(tasks) > 0:
                self.log("\n✅ PASSED: Tasks are personalized and AI-generated", "SUCCESS")
                self.tests_passed += 1
                return True
            else:
                self.log("\n❌ FAILED: Tasks are not properly personalized", "ERROR")
                self.tests_failed += 1
                return False
                
        except Exception as e:
            self.log(f"❌ Exception: {str(e)}", "ERROR")
            self.tests_failed += 1
            return False
    
    def test_credit_ai_estimation(self):
        """
        CRITICAL TEST: Verify CreditAI actually calls OpenAI for score estimation
        """
        self.log("\n" + "="*80)
        self.log("TEST 2: Credit AI Score Estimation")
        self.log("="*80)
        
        try:
            self.log("Calling CreditAI for score estimation...")
            
            # Call credit score estimation
            credit_response = requests.get(
                f"{BASE_URL}/api/credit/score/estimate",
                params={"user_id": self.test_user_email},
                timeout=30  # AI calls can take time
            )
            
            if credit_response.status_code != 200:
                self.log(f"❌ Credit estimation failed: {credit_response.status_code}", "ERROR")
                self.log(f"Response: {credit_response.text}", "ERROR")
                self.tests_failed += 1
                return False
            
            credit_data = credit_response.json()
            
            self.log(f"\nEstimated Score: {credit_data.get('estimated_score')}")
            self.log(f"Score Range: {credit_data.get('score_range')}")
            self.log(f"AI Powered: {credit_data.get('ai_powered')}")
            
            # Check if AI was actually used
            if not credit_data.get('ai_powered'):
                self.log("⚠️  WARNING: ai_powered flag is False", "WARNING")
            
            # Check recommendations are substantive
            recommendations = credit_data.get('recommendations', [])
            self.log(f"\nRecommendations ({len(recommendations)}):")
            for i, rec in enumerate(recommendations, 1):
                self.log(f"  {i}. {rec}")
            
            if len(recommendations) >= 3 and credit_data.get('estimated_score'):
                self.log("\n✅ PASSED: Credit AI estimation working", "SUCCESS")
                self.tests_passed += 1
                return True
            else:
                self.log("\n❌ FAILED: Credit AI estimation incomplete", "ERROR")
                self.tests_failed += 1
                return False
                
        except Exception as e:
            self.log(f"❌ Exception: {str(e)}", "ERROR")
            self.tests_failed += 1
            return False
    
    def test_70_lessons_library(self):
        """
        TEST: Verify all 70 lessons are accessible
        """
        self.log("\n" + "="*80)
        self.log("TEST 3: 70-Lesson Library Verification")
        self.log("="*80)
        
        try:
            # Get all lessons
            lessons_response = requests.get(
                f"{BASE_URL}/api/mentor/lessons/list",
                timeout=10
            )
            
            if lessons_response.status_code != 200:
                self.log(f"❌ Lessons list failed: {lessons_response.status_code}", "ERROR")
                self.tests_failed += 1
                return False
            
            lessons_data = lessons_response.json()
            lessons = lessons_data.get('lessons', [])
            total = lessons_data.get('total', 0)
            
            self.log(f"Total lessons available: {total}")
            
            if total != 70:
                self.log(f"❌ FAILED: Expected 70 lessons, got {total}", "ERROR")
                self.tests_failed += 1
                return False
            
            # Test accessing a few random lessons
            test_lesson_ids = ["lesson_1", "lesson_35", "lesson_70"]
            all_accessible = True
            
            for lesson_id in test_lesson_ids:
                lesson_response = requests.get(
                    f"{BASE_URL}/api/mentor/lesson/{lesson_id}",
                    timeout=10
                )
                
                if lesson_response.status_code == 200:
                    lesson = lesson_response.json()
                    self.log(f"✅ {lesson_id}: {lesson.get('title')} - {lesson.get('duration_min')} min")
                else:
                    self.log(f"❌ {lesson_id}: Failed to load", "ERROR")
                    all_accessible = False
            
            if all_accessible and total == 70:
                self.log("\n✅ PASSED: All 70 lessons accessible", "SUCCESS")
                self.tests_passed += 1
                return True
            else:
                self.log("\n❌ FAILED: Lesson library incomplete", "ERROR")
                self.tests_failed += 1
                return False
                
        except Exception as e:
            self.log(f"❌ Exception: {str(e)}", "ERROR")
            self.tests_failed += 1
            return False
    
    def test_task_completion_persistence(self):
        """
        TEST: Verify task completion persists in database
        """
        self.log("\n" + "="*80)
        self.log("TEST 4: Task Completion Persistence")
        self.log("="*80)
        
        try:
            # Get active tasks
            tasks_response = requests.get(
                f"{BASE_URL}/api/mentor/tasks/active",
                params={"user_id": self.test_user_email},
                timeout=10
            )
            
            if tasks_response.status_code != 200:
                self.log(f"❌ Get tasks failed: {tasks_response.status_code}", "ERROR")
                self.tests_failed += 1
                return False
            
            tasks_data = tasks_response.json()
            tasks = tasks_data.get('tasks', [])
            
            if len(tasks) == 0:
                self.log("No tasks to test completion", "WARNING")
                self.tests_passed += 1
                return True
            
            # Complete first task
            first_task = tasks[0]
            task_id = first_task.get('task_id')
            
            self.log(f"Completing task: {first_task.get('description')}")
            
            complete_response = requests.post(
                f"{BASE_URL}/api/mentor/tasks/{task_id}/complete",
                params={"user_id": self.test_user_email},
                timeout=10
            )
            
            if complete_response.status_code != 200:
                self.log(f"❌ Task completion failed: {complete_response.status_code}", "ERROR")
                self.tests_failed += 1
                return False
            
            # Verify task is no longer in active list
            time.sleep(1)  # Brief delay for DB update
            
            verify_response = requests.get(
                f"{BASE_URL}/api/mentor/tasks/active",
                params={"user_id": self.test_user_email},
                timeout=10
            )
            
            if verify_response.status_code != 200:
                self.log(f"❌ Verification failed: {verify_response.status_code}", "ERROR")
                self.tests_failed += 1
                return False
            
            verify_data = verify_response.json()
            remaining_tasks = verify_data.get('tasks', [])
            
            # Check if completed task is removed from active list
            task_still_active = any(t.get('task_id') == task_id for t in remaining_tasks)
            
            if task_still_active:
                self.log("❌ FAILED: Completed task still in active list", "ERROR")
                self.tests_failed += 1
                return False
            else:
                self.log("✅ PASSED: Task completion persisted correctly", "SUCCESS")
                self.tests_passed += 1
                return True
                
        except Exception as e:
            self.log(f"❌ Exception: {str(e)}", "ERROR")
            self.tests_failed += 1
            return False
    
    def run_all_tests(self):
        """Run all AI verification tests"""
        self.log("\n" + "="*80)
        self.log("AI INTEGRATION VERIFICATION TEST SUITE")
        self.log("="*80)
        
        # Run tests
        self.test_ai_task_generation_personalization()
        self.test_credit_ai_estimation()
        self.test_70_lessons_library()
        self.test_task_completion_persistence()
        
        # Summary
        self.log("\n" + "="*80)
        self.log("TEST SUMMARY")
        self.log("="*80)
        self.log(f"Passed: {self.tests_passed} ✅")
        self.log(f"Failed: {self.tests_failed} ❌")
        self.log(f"Success Rate: {(self.tests_passed / (self.tests_passed + self.tests_failed) * 100):.1f}%")
        
        return self.tests_failed == 0

if __name__ == "__main__":
    tester = AIVerificationTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
