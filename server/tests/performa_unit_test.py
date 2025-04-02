import unittest
from unittest.mock import patch
from flask import json
import os
import sys
from datetime import datetime, timedelta, timezone

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from performa import app, db
from models.user.user import User
from models.user.user_role import UserRole
from models.user.user_token import UserToken

class TestLogin(unittest.TestCase):
    def setUp(self):
        # Configure test app with in-memory SQLite
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        
        self.client = app.test_client()
        
        # Create test database
        with app.app_context():
            db.create_all()
            
            # Create all required roles first
            roles = [
                UserRole(id=1, name="STUDENT"),
                UserRole(id=2, name="INSTRUCTOR"),
                UserRole(id=3, name="ADMIN")
            ]
            db.session.add_all(roles)
            db.session.commit()
            
            # Create test user
            user = User(
                id=9999,
                email="testuser@conestogac.on.ca",
                first_name="Test",
                last_name="User",
                role_id=1,  # Matches STUDENT role
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

    @patch('models.user.user_token.generate_otp', return_value="123456")
    def test_send_otp_success(self, mock_otp):
        """Test successful OTP sending"""
        response = self.client.post(
            '/api/send-otp',
            json={'email': 'testuser@conestogac.on.ca'}
        )
        print("Response data:", response.data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['code'], 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['data'], "123456")  # Should match mocked OTP

    def test_send_otp_invalid_email(self):
        """Test OTP sending with invalid email"""
        response = self.client.post(
            '/api/send-otp',
            json={'email': 'nonexistent@conestogac.on.ca'}
        )
        print("Response data:", response.data)
        self.assertEqual(response.status_code, 500)  # Your API returns 500 for this case
        data = json.loads(response.data)
        self.assertEqual(data['code'], 500)
        self.assertFalse(data['success'])
        self.assertEqual(data['data']['err_msg'], "email nonexistent@conestogac.on.ca not found")

    def test_send_otp_inactive_user(self):
        """Test OTP sending for inactive user"""
        with app.app_context():
            user = db.session.get(User, 9999)
            user.is_active = False
            db.session.commit()
        
        response = self.client.post(
            '/api/send-otp',
            json={'email': 'testuser@conestogac.on.ca'}
        )
        print("Response data:", response.data)
        self.assertEqual(response.status_code, 500)  # Your API returns 500 for this case
        data = json.loads(response.data)
        self.assertEqual(data['code'], 500)
        self.assertFalse(data['success'])
        self.assertEqual(data['data']['err_msg'], "inactive user testuser@conestogac.on.ca")

    @patch('models.user.user_token.generate_otp', return_value="123456")
    def test_verify_otp_success(self, mock_otp):
        """Test successful OTP verification"""
        # First send OTP
        self.client.post('/api/send-otp',
                       json={'email': 'testuser@conestogac.on.ca'})
        
        # Then verify
        response = self.client.post(
            '/api/login',
            json={
                'email': 'testuser@conestogac.on.ca',
                'otp': '123456'
            }
        )
        print("Response data:", response.data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['code'], 200)
        self.assertTrue(data['success'])
        self.assertIn('token', data['data'])

    @patch('models.user.user_token.utcnow')
    def test_verify_otp_expired(self, mock_utcnow):
        """Test expired OTP verification"""
        # Mock future time to make OTP expired
        mock_utcnow.return_value = datetime.now(timezone.utc) + timedelta(minutes=10)
        
        self.client.post('/api/send-otp',
                       json={'email': 'testuser@conestogac.on.ca'})
        
        response = self.client.post(
            '/api/login',
            json={
                'email': 'testuser@conestogac.on.ca',
                'otp': '123456'
            }
        )
        print("Response data:", response.data)
        self.assertEqual(response.status_code, 500)  # Your API returns 500 for this case
        data = json.loads(response.data)
        self.assertEqual(data['code'], 500)
        self.assertFalse(data['success'])
        self.assertEqual(data['data']['err_msg'], "Invalid credentials")

    def test_verify_otp_invalid(self):
        """Test invalid OTP verification"""
        self.client.post('/api/send-otp',
                       json={'email': 'testuser@conestogac.on.ca'})
        
        response = self.client.post(
            '/api/login',
            json={
                'email': 'testuser@conestogac.on.ca',
                'otp': 'wrong_otp'
            }
        )
        print("Response data:", response.data)
        self.assertEqual(response.status_code, 500)  # Your API returns 500 for this case
        data = json.loads(response.data)
        self.assertEqual(data['code'], 500)
        self.assertFalse(data['success'])
        self.assertEqual(data['data']['err_msg'], "Invalid credentials")

if __name__ == '__main__':
    unittest.main()