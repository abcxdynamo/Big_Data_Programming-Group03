import unittest
from flask import json
import os
import sys
from datetime import datetime, timedelta, timezone
from colorama import Fore, Style, init
import random
import string

# Initialize colorama
init()

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from performa import app, db
from models.grade.grade import Grade
from models.user.user import User
from models.course.course import Course
from models.course.term import Term
from models.course.program import Program

class TestGrade(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print(f"\n{Fore.CYAN}=== Starting Performa Grade Tests ==={Style.RESET_ALL}\n")
        # Configure test app
        cls.app = app
        cls.app.config['TESTING'] = True
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        cls.app.config['WTF_CSRF_ENABLED'] = False
        
        # Push application context
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        
        # Create all tables
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        # Clean up test data
        with cls.app.app_context():
            # Delete in proper order to respect foreign key constraints
            Grade.query.delete()
            Course.query.delete()
            Term.query.delete()
            Program.query.delete()
            User.query.delete()
            db.session.commit()
        
        # Remove the app context
        db.session.remove()
        cls.app_context.pop()

    def setUp(self):
        self.client = self.app.test_client()
        # Start a transaction
        db.session.begin()
        self.create_test_data()

    def tearDown(self):
        # Rollback the transaction to undo any changes
        db.session.rollback()

    def create_test_data(self):
        """Create test data with unique constraints handled"""
        try:
            # Generate more unique identifiers
            timestamp = str(int(datetime.now().timestamp()))[-6:]
            rand_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            
            # Create test user
            self.test_user = User(
                email=f"user{timestamp}{rand_str}@conestogac.on.ca",
                first_name="Test",
                last_name=f"User{rand_str}",
                role_id=1,
                is_active=True,
                create_time=datetime.now(timezone.utc),
                update_time=datetime.now(timezone.utc),
                is_deleted=False
            )
            db.session.add(self.test_user)
            db.session.flush()  # Flush to get the ID
            
            # Create test program with unique name
            self.test_program = Program(
                name=f"Program {timestamp}{rand_str}",
                code=f"PRG{timestamp}{rand_str[:3]}"[:10],
                description=f"Description {rand_str}",
                co_op=False,
                create_time=datetime.now(timezone.utc),
                update_time=datetime.now(timezone.utc),
                is_deleted=False
            )
            db.session.add(self.test_program)
            db.session.flush()
            
            # Create test term with guaranteed unique year-season combination
            current_year = datetime.now().year
            self.test_term = Term(
                year=current_year + int(timestamp[:2]),  # More variation in years
                season=f"Season{rand_str[:2]}",  # Ensure unique season
                section=int(timestamp[-1]),
                start_date=datetime.now(timezone.utc),
                end_date=datetime.now(timezone.utc) + timedelta(days=90),
                create_time=datetime.now(timezone.utc),
                update_time=datetime.now(timezone.utc),
                is_deleted=False
            )
            db.session.add(self.test_term)
            db.session.flush()
            
            # Create test course with unique code
            self.test_course = Course(
                name=f"Course {timestamp}{rand_str}",
                code=f"CRS{timestamp}{rand_str[:3]}",
                description=f"Description {rand_str}",
                create_time=datetime.now(timezone.utc),
                update_time=datetime.now(timezone.utc),
                is_deleted=False
            )
            db.session.add(self.test_course)
            db.session.flush()
            
            # Create test grade
            self.test_grade = Grade(
                student_id=self.test_user.id,
                course_id=self.test_course.id,
                term_id=self.test_term.id,
                program_id=self.test_program.id,
                final_grade=10,
                feedback="Initial feedback",
                create_time=datetime.now(timezone.utc),
                update_time=datetime.now(timezone.utc),
                is_deleted=False
            )
            db.session.add(self.test_grade)
            
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            print(f"{Fore.RED}Error creating test data: {str(e)}{Style.RESET_ALL}")
            raise

    def test_get_grade_success(self):
        """Test successful grade retrieval"""
        print(f"{Fore.YELLOW}➤ Testing grade retrieval...{Style.RESET_ALL}", end=" ")
        try:
            # Verify test data exists first
            grade = Grade.query.filter_by(
                student_id=self.test_user.id,
                course_id=self.test_course.id,
                term_id=self.test_term.id
            ).first()
            self.assertIsNotNone(grade, "Test grade should exist")
            
            response = self.client.get(
                f'/api/grades/{self.test_user.id}/{self.test_course.id}/{self.test_term.id}'
            )
            print(f"Response: {response.status_code}, Data: {response.data}")  # Debug
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['code'], 200)
            self.assertTrue(data['success'])
            self.assertEqual(data['data']['final_grade'], 10)
            print(f"{Fore.GREEN}PASSED{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}FAILED: {str(e)}{Style.RESET_ALL}")
            raise

    def test_get_grade_not_found(self):
        """Test grade retrieval with non-existing grade"""
        print(f"{Fore.YELLOW}➤ Testing grade retrieval for non-existent grade...{Style.RESET_ALL}", end=" ")
        try:
            response = self.client.get('/api/grades/999999/999999/999999')
            print(f"Response: {response.status_code}, Data: {response.data}")  # Debug
            self.assertEqual(response.status_code, 404)
            data = json.loads(response.data)
            self.assertEqual(data['code'], 404)
            self.assertFalse(data['success'])
            self.assertEqual(data['data']['err_msg'], "Grade not found")
            print(f"{Fore.GREEN}PASSED{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}FAILED: {str(e)}{Style.RESET_ALL}")
            raise

    # def test_save_grade_feedback_success(self):
    #     """Test successful grade feedback saving"""
    #     print(f"{Fore.YELLOW}➤ Testing grade feedback saving...{Style.RESET_ALL}", end=" ")
    #     try:
    #         # Verify test grade exists
    #         grade = Grade.query.get(self.test_grade.id)
    #         self.assertIsNotNone(grade, "Test grade should exist")
            
    #         response = self.client.post(
    #             f'/api/grades/{self.test_grade.id}/feedback',
    #             json={'feedback': 'Great improvement!'}
    #         )
    #         print(f"Response: {response.status_code}, Data: {response.data}")  # Debug
    #         self.assertEqual(response.status_code, 200)
    #         data = json.loads(response.data)
    #         self.assertEqual(data['code'], 200)
    #         self.assertTrue(data['success'])
    #         self.assertEqual(data['data']['feedback'], 'Great improvement!')
    #         print(f"{Fore.GREEN}PASSED{Style.RESET_ALL}")
    #     except Exception as e:
    #         print(f"{Fore.RED}FAILED: {str(e)}{Style.RESET_ALL}")
    #         raise

    def test_save_grade_feedback_failure(self):
        """Test failure when saving grade feedback for non-existing grade"""
        print(f"{Fore.YELLOW}➤ Testing saving feedback for non-existing grade...{Style.RESET_ALL}", end=" ")
        try:
            response = self.client.post(
                '/api/grades/999999/feedback',
                json={'feedback': 'Feedback not found!'}
            )
            print(f"Response: {response.status_code}, Data: {response.data}")  # Debug
            self.assertEqual(response.status_code, 404)
            data = json.loads(response.data)
            self.assertEqual(data['code'], 404)
            self.assertFalse(data['success'])
            self.assertEqual(data['data']['err_msg'], "Grade not found")
            print(f"{Fore.GREEN}PASSED{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}FAILED: {str(e)}{Style.RESET_ALL}")
            raise

    # def test_update_grade_success(self):
    #     """Test successful grade update"""
    #     print(f"{Fore.YELLOW}➤ Testing grade update...{Style.RESET_ALL}", end=" ")
    #     try:
    #         # Verify test grade exists
    #         grade = Grade.query.get(self.test_grade.id)
    #         self.assertIsNotNone(grade, "Test grade should exist")
            
    #         response = self.client.put(
    #             f'/api/grades/{self.test_grade.id}',
    #             json={'final_grade': 11, 'feedback': 'Excellent work!'}
    #         )
    #         print(f"Response: {response.status_code}, Data: {response.data}")  # Debug
    #         self.assertEqual(response.status_code, 200)
    #         data = json.loads(response.data)
    #         self.assertEqual(data['code'], 200)
    #         self.assertTrue(data['success'])
    #         self.assertEqual(data['data']['final_grade'], 11)
    #         self.assertEqual(data['data']['feedback'], 'Excellent work!')
    #         print(f"{Fore.GREEN}PASSED{Style.RESET_ALL}")
    #     except Exception as e:
    #         print(f"{Fore.RED}FAILED: {str(e)}{Style.RESET_ALL}")
    #         raise

if __name__ == '__main__':
    # Create a test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestGrade)
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=0)
    result = runner.run(suite)
    
    # Print beautiful summary
    print(f"\n{Fore.CYAN}=== Test Summary ==={Style.RESET_ALL}")
    print(f"{Fore.GREEN}✓ PASSED: {result.testsRun - len(result.failures) - len(result.errors)}{Style.RESET_ALL}")
    if result.failures:
        print(f"{Fore.RED}✗ FAILED: {len(result.failures)}{Style.RESET_ALL}")
    if result.errors:
        print(f"{Fore.RED}⚠ ERRORS: {len(result.errors)}{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}=== Final Result ==={Style.RESET_ALL}")
    if result.wasSuccessful():
        print(f"{Fore.GREEN}✔ ALL TESTS PASSED SUCCESSFULLY!{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}✖ SOME TESTS FAILED OR HAD ERRORS{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}Total tests run: {result.testsRun}{Style.RESET_ALL}")