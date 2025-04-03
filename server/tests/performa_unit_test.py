import unittest
from unittest.mock import patch
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
        
        # Create test database
        with app.app_context():
            db.drop_all()
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

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_send_otp_success(self):
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

    def test_send_otp_invalid_email(self):
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

    def test_send_otp_inactive_user(self):
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

    def test_verify_otp_success(self):
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

    def test_verify_otp_expired(self):
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

    def test_verify_otp_invalid(self):
        """Test invalid OTP verification"""
        print(f"{Fore.YELLOW}➤ Testing invalid OTP verification...{Style.RESET_ALL}", end=" ")
        self.client.post('/api/send-otp',
                       json={'email': 'testuser@conestogac.on.ca'})
        
        response = self.client.post(
            '/api/login',
            json={
                'email': 'testuser@conestogac.on.ca',
                'otp': 'wrong_otp'
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
    