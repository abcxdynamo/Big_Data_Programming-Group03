import sys 
import os
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta, timezone

# Ensure the `server` folder is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the Flask app and services
from performa import app
from services.user_service import UserService
from models.user.user import User
from models.user.user_token import UserToken
from models.user.user_role import UserRole
from utils.auth import generate_jwt_token

class TestUserService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Ensure the Flask app context is active for all test cases"""
        cls.app_context = app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        """Remove the app context after all tests are done"""
        cls.app_context.pop()

    def setUp(self):
        """Set up test client and reset mocks"""
        self.client = app.test_client()
        
        # Mock send_email function
        self.patcher_send_email = patch('services.user_service.send_email', return_value=None)
        self.mock_send_email = self.patcher_send_email.start()
        
        # Common mock user data
        self.mock_user = MagicMock()
        self.mock_user.is_active = True
        self.mock_user.email = 'test@example.com'
        self.mock_user.id = 1
        self.mock_user.role_id = 1

        # Mock utcnow for token expiration (using timezone-aware datetime)
        self.patcher_utcnow = patch('services.user_service.utcnow')
        self.mock_utcnow = self.patcher_utcnow.start()
        self.mock_utcnow.return_value = datetime.now(timezone.utc)

    def tearDown(self):
        """Stop all active patches"""
        patch.stopall()

    @patch('services.user_service.UserService.get_user_by_email')
    @patch('services.user_service.UserToken')
    def test_send_otp(self, mock_user_token, mock_get_user_by_email):
        print("Starting test_send_otp...")

        # Mock user
        mock_get_user_by_email.return_value = self.mock_user

        # Mock UserToken instance with proper expiration
        mock_token_instance = MagicMock()
        mock_token_instance.otp = '444601'
        mock_token_instance.expires = datetime.now(timezone.utc) + timedelta(minutes=15)
        mock_token_instance.save = MagicMock()
        mock_user_token.return_value = mock_token_instance

        # Mock query to return None (no existing token)
        with patch('services.user_service.UserToken.query') as mock_query:
            mock_filter = MagicMock()
            mock_filter.first.return_value = None
            mock_query.filter.return_value = mock_filter

            # Call the method
            otp = UserService.send_otp('test@example.com')

        # Assertions
        self.mock_send_email.assert_called_once()
        mock_token_instance.save.assert_called_once()
        self.assertEqual(otp, '444601')
        print("Completed test_send_otp...")

    @patch('services.user_service.UserService.get_user_by_email')
    @patch('services.user_service.generate_jwt_token')
    @patch('services.user_service.UserRole')
    def test_validate_otp(self, mock_user_role, mock_generate_jwt_token, mock_get_user_by_email):
        print("Starting test_validate_otp...")

        # Setup mocks
        mock_get_user_by_email.return_value = self.mock_user
        mock_user_role.get_name_by_id.return_value = 'admin'
        mock_generate_jwt_token.return_value = 'mock_token'

        # Create a mock user token with proper expiration
        mock_user_token = MagicMock()
        mock_user_token.otp = '123456'
        mock_user_token.token = None
        mock_user_token.expires = datetime.now(timezone.utc) + timedelta(minutes=15)
        mock_user_token.save = MagicMock()

        # Mock the query to return our token
        with patch('services.user_service.UserToken.query') as mock_query:
            mock_filter_by = MagicMock()
            mock_filter_by.first.return_value = mock_user_token
            mock_query.filter_by.return_value = mock_filter_by

            # Test valid OTP
            result = UserService.validate_otp('test@example.com', '123456')

        # Assertions
        mock_generate_jwt_token.assert_called_once_with({
            'user_id': self.mock_user.id,
            'email': self.mock_user.email,
            'role_id': self.mock_user.role_id,
            'role_name': 'admin'
        })
        mock_user_token.save.assert_called_once()
        self.assertEqual(result['token'], 'mock_token')
        print("Completed test_validate_otp...")

    @patch('services.user_service.UserService.get_user_by_email')
    def test_validate_otp_invalid(self, mock_get_user_by_email):
        print("Starting test_validate_otp_invalid...")
        
        # Setup mocks
        mock_get_user_by_email.return_value = self.mock_user
        
        # Mock query to return None (no token found)
        with patch('services.user_service.UserToken.query') as mock_query:
            mock_filter_by = MagicMock()
            mock_filter_by.first.return_value = None
            mock_query.filter_by.return_value = mock_filter_by

            # Test with invalid OTP (should raise AssertionError)
            with self.assertRaises(AssertionError) as context:
                UserService.validate_otp('test@example.com', 'wrong_otp')
            
            self.assertEqual(str(context.exception), "Invalid credentials")
        
        print("Completed test_validate_otp_invalid...")

if __name__ == '__main__':
    unittest.main()