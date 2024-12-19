from django.test import TestCase, Client
from django.urls import reverse
from Travel.models import Person

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create test person with all required fields
        self.test_person = Person.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='testpass123',
            confirm_password='testpass123',
            age=25
        )

    def test_signup_success(self):
        """Test successful user registration"""
        signup_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'confirm-password': 'newpass123',
            'age': 30
        }
        
        try:
            response = self.client.post('/signup/', signup_data)
            print(f"\nSignup Test (Success Case)")
            print(f"Response Status Code: {response.status_code}")
            print(f"Status: {'Success' if response.status_code == 200 else 'Failed'}")
            
            # Verify user was created
            user = Person.objects.filter(email='newuser@example.com').first()
            if user:
                print(f"User Created: Yes")
                print(f"Username: {user.username}")
                print(f"Email: {user.email}")
            else:
                print("User Created: No")
            
            self.assertTrue(user is not None)
            self.assertEqual(user.username, 'newuser')
            self.assertEqual(user.email, 'newuser@example.com')
            self.assertEqual(response.status_code, 200)
            
        except Exception as e:
            print(f"\nError during signup test: {str(e)}")
            raise

    def test_login_success(self):
        """Test successful login"""
        login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        try:
            response = self.client.post('/login/', login_data)
            print(f"\nLogin Test (Success Case)")
            print(f"Response Status Code: {response.status_code}")
            print(f"Status: {'Success' if response.status_code == 200 else 'Failed'}")
            
            self.assertEqual(response.status_code, 200)
            
        except Exception as e:
            print(f"\nError during login test: {str(e)}")
            raise

    def test_login_invalid_credentials(self):
        """Test login with wrong password"""
        login_data = {
            'username': 'testuser',
            'password': 'wrongpass'
        }
        
        try:
            response = self.client.post('/login/', login_data)
            print(f"\nLogin Test (Invalid Credentials)")
            print(f"Response Status Code: {response.status_code}")
            print(f"Status: {'Success' if response.status_code == 200 else 'Failed'}")
            
            self.assertEqual(response.status_code, 200)
            self.assertIn('User does not exist', response.content.decode())
            
        except Exception as e:
            print(f"\nError during invalid login test: {str(e)}")
            raise

    def test_book_form(self):
        """Test booking form submission"""
        book_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '1234567890',
            'numpeople': '2'
        }
        
        try:
            response = self.client.post('/form/', book_data)
            print(f"\nBooking Form Test")
            print(f"Response Status Code: {response.status_code}")
            print(f"Status: {'Success' if response.status_code == 200 else 'Failed'}")
            
            self.assertEqual(response.status_code, 200)
            self.assertIn('Submit Successful', response.content.decode())
            
        except Exception as e:
            print(f"\nError during booking test: {str(e)}")
            raise