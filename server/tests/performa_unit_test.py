import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from flask import json
import os
import sys
from datetime import datetime, timedelta, timezone
from colorama import Fore, Style, init

# Initialize colorama
init()

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from performa import app, db
from models.user.user import User
from models.user.user_role import UserRole
from models.user.user_token import UserToken
from models.grade.grade import Grade
from task import grade_prediction

class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print(f"\n{Fore.CYAN}=== Starting Performa Login Tests ==={Style.RESET_ALL}\n")

    def setUp(self):
        # Configure test app with in-memory SQLite
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        
        self.client = app.test_client()
        
        # Create test database and insert initial data
        with app.app_context():
            db.create_all()
            
            if not db.session.query(UserRole).filter_by(id=1).first():
                roles = [
                    UserRole(id=1, name="STUDENT"),
                    UserRole(id=2, name="INSTRUCTOR"),
                    UserRole(id=3, name="ADMIN")
                ]
                db.session.bulk_save_objects(roles)
            
            if not db.session.query(User).filter_by(id=9999).first():
                user = User(
                    id=9999,
                    email="testuser@conestogac.on.ca",
                    first_name="Test",
                    last_name="User",
                    role_id=1,
                    is_active=True,
                    create_time=datetime.now(timezone.utc),
                    update_time=datetime.now(timezone.utc),
                    is_deleted=False
                )
                db.session.add(user)
                db.session.commit()
                
            # Create test grade
            self.test_grade = Grade(
                student_id=9999,
                tp_course_id=1,
                final_grade=85.5,
                final_gpa=3.7,
                feedback="Initial feedback",
                create_time=datetime.now(timezone.utc),
                update_time=datetime.now(timezone.utc),
                is_deleted=False
            )
            db.session.add(self.test_grade)

            db.session.commit()

    def tearDown(self):
        with app.app_context():
            # Delete only tokens related to the test user to avoid FK issues
            db.session.query(UserToken).filter_by(user_id=9999).delete()
            db.session.query(Grade).filter_by(student_id=9999).delete()
            # Reset the user to active in case a test deactivated it
            user = db.session.query(User).filter_by(id=9999).first()
            if user:
                user.is_active = True
                db.session.commit()

            db.session.remove()
            
    def test_01_send_otp_success(self):
        """Test successful OTP sending"""
        print(f"{Fore.YELLOW}➤ Testing valid OTP request...{Style.RESET_ALL}", end=" ")
        response = self.client.post(
            '/api/send-otp',
            json={'email': 'testuser@conestogac.on.ca'}
        )
        data = json.loads(response.data)
        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['code'], 200)
            self.assertTrue(data['success'])
            self.assertIsInstance(data['data'], str)
            print(f"{Fore.GREEN}PASSED{Style.RESET_ALL}")
        except AssertionError:
            print(f"{Fore.RED}FAILED{Style.RESET_ALL}")
            raise

    def test_02_send_otp_invalid_email(self):
        """Test OTP sending with invalid email"""
        print(f"{Fore.YELLOW}➤ Testing invalid email request...{Style.RESET_ALL}", end=" ")
        response = self.client.post(
            '/api/send-otp',
            json={'email': 'nonexistent@conestogac.on.ca'}
        )
        data = json.loads(response.data)
        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['code'], 500)
            self.assertFalse(data['success'])
            self.assertEqual(data['data']['err_msg'], "email nonexistent@conestogac.on.ca not found")
            print(f"{Fore.GREEN}PASSED{Style.RESET_ALL}")
        except AssertionError:
            print(f"{Fore.RED}FAILED{Style.RESET_ALL}")
            raise

    def test_03_send_otp_inactive_user(self):
        """Test OTP sending for inactive user"""
        print(f"{Fore.YELLOW}➤ Testing inactive user request...{Style.RESET_ALL}", end=" ")
        with app.app_context():
            user = db.session.query(User).filter_by(id=9999).first()
            user.is_active = False
            db.session.commit()
        
        response = self.client.post(
            '/api/send-otp',
            json={'email': 'testuser@conestogac.on.ca'}
        )
        data = json.loads(response.data)
        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['code'], 500)
            self.assertFalse(data['success'])
            self.assertEqual(data['data']['err_msg'], "inactive user testuser@conestogac.on.ca")
            print(f"{Fore.GREEN}PASSED{Style.RESET_ALL}")
        except AssertionError:
            print(f"{Fore.RED}FAILED{Style.RESET_ALL}")
            raise

    def test_04_verify_otp_success(self):
        """Test successful OTP verification"""
        print(f"{Fore.YELLOW}➤ Testing valid OTP verification...{Style.RESET_ALL}", end=" ")
        otp_response = self.client.post(
            '/api/send-otp',
            json={'email': 'testuser@conestogac.on.ca'}
        )
        otp = json.loads(otp_response.data)['data']
        
        response = self.client.post(
            '/api/login',
            json={
                'email': 'testuser@conestogac.on.ca',
                'otp': otp
            }
        )
        data = json.loads(response.data)
        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['code'], 200)
            self.assertTrue(data['success'])
            self.assertIn('token', data['data'])
            print(f"{Fore.GREEN}PASSED{Style.RESET_ALL}")
        except AssertionError:
            print(f"{Fore.RED}FAILED{Style.RESET_ALL}")
            raise

    def test_05_verify_otp_expired(self):
        """Test expired OTP verification"""
        print(f"{Fore.YELLOW}➤ Testing expired OTP verification...{Style.RESET_ALL}", end=" ")
        self.client.post('/api/send-otp',
                         json={'email': 'testuser@conestogac.on.ca'})
        
        with patch('models.user.user_token.utcnow') as mock_utcnow:
            mock_utcnow.return_value = datetime.now(timezone.utc) + timedelta(minutes=10)
            response = self.client.post(
                '/api/login',
                json={
                    'email': 'testuser@conestogac.on.ca',
                    'otp': 'anycode'
                }
            )
        
        data = json.loads(response.data)
        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['code'], 500)
            self.assertFalse(data['success'])
            self.assertEqual(data['data']['err_msg'], "Invalid credentials")
            print(f"{Fore.GREEN}PASSED{Style.RESET_ALL}")
        except AssertionError:
            print(f"{Fore.RED}FAILED{Style.RESET_ALL}")
            raise
        
    def test_06_get_grade_success(self):
        """Test successful grade retrieval"""
        print(f"{Fore.YELLOW}➤ Testing grade retrieval...{Style.RESET_ALL}", end=" ")
        try:
            response = self.client.get(
                f'/api/grades/1/1?student_id=9999&course_id=1'
            )
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['code'], 200)
            self.assertTrue(data['success'])
            self.assertIn('data', data)
            grade_data = data['data']
        # If the response is a list, we need to loop through to check each item
            for grade in grade_data:
                self.assertIn('final_grade', grade)  # Check if 'final_grade' exists
                self.assertIn('final_gpa', grade)    # Check if 'final_gpa' exists
                self.assertEqual(grade['final_grade'], 85.5)  # Validate the value of final_grade
                self.assertEqual(grade['final_gpa'], 3.7)     # Validate the value of final_gpa
            print(f"{Fore.GREEN}PASSED{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}FAILED: {str(e)}{Style.RESET_ALL}")
            raise

    def test_07_get_grade_not_found(self):
        """Test grade retrieval with non-existing grade"""
        print(f"{Fore.YELLOW}➤ Testing grade retrieval for non-existent grade...{Style.RESET_ALL}", end=" ")
        try:
            response = self.client.get('/api/grades/1/1?student_id=9999&course_id=2') # No grade added for course_id=2
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['code'], 200)
            self.assertTrue(data['success'])
            self.assertEqual(data['data'], []) # No record returned
            print(f"{Fore.GREEN}PASSED{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}FAILED: {str(e)}{Style.RESET_ALL}")
            raise
        
    def test_08_get_training_data(self):
        """Test for fetching training data from DB"""
        print(f"{Fore.YELLOW}➤ Testing get_training_data...{Style.RESET_ALL}", end=" ")
        
        mock_conn = MagicMock()
        mock_conn.execute.return_value = None
        mock_conn.fetchall.return_value = []

        mock_df = pd.DataFrame({
            'program_id': [1],
            'program_level': [2],
            'credits': [3],
            'attendance_percent': [90],
            'final_grade': [85],
            'course_id': [101]
        })

        with patch('pandas.read_sql', return_value=mock_df):
            df = grade_prediction.get_training_data()
            print("Fetched DataFrame:", df)
            
            try:
                self.assertFalse(df.empty)
                self.assertEqual(df.iloc[0]['final_grade'], 85)
                print(f"{Fore.GREEN}PASSED{Style.RESET_ALL}")
            except AssertionError:
                print(f"{Fore.RED}FAILED{Style.RESET_ALL}")
                raise
            
    def test_09_grade_to_gpa(self):
        """Test for grade to GPA conversion"""
        print(f"{Fore.YELLOW}➤ Testing grade_to_gpa...{Style.RESET_ALL}", end=" ")
        
        try:
            self.assertEqual(grade_prediction.grade_to_gpa(95), 4.0)
            self.assertEqual(grade_prediction.grade_to_gpa(80), 3.75)
            self.assertEqual(grade_prediction.grade_to_gpa(65), 2.5)
            self.assertEqual(grade_prediction.grade_to_gpa(50), 0.0)
            print(f"{Fore.GREEN}PASSED{Style.RESET_ALL}")
        except AssertionError:
            print(f"{Fore.RED}FAILED{Style.RESET_ALL}")
            raise

    @patch('task.grade_prediction.get_training_data')
    @patch('task.grade_prediction.engine.connect')
    def test_10_predict_and_update_gpa_no_terms(self, mock_connect, mock_get_training_data):
        """Test predict_and_update_gpa when there are no terms"""
        print(f"{Fore.YELLOW}➤ Testing predict_and_update_gpa_no_terms...{Style.RESET_ALL}", end=" ")

        mock_get_training_data.return_value = pd.DataFrame({
            'program_id': [1],
            'program_level': [2],
            'credits': [3],
            'attendance_percent': [90],
            'final_grade': [85],
            'course_id': [101]
        })

        mock_conn = MagicMock()
        mock_conn.execute.return_value = None

        with patch('pandas.read_sql', return_value=pd.DataFrame({'id': []})):
            grade_prediction.predict_and_update_gpa()
            mock_conn.execute.assert_not_called()
            print(f"{Fore.GREEN}PASSED{Style.RESET_ALL}")
            
if __name__ == '__main__':
    # Create a test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestLogin)
    
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
