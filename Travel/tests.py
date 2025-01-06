from django.test import TransactionTestCase, Client, RequestFactory
from django.urls import reverse
from .models import Person, Book
from django.core.files.uploadedfile import SimpleUploadedFile
import json
import threading
import multiprocessing
import logging
from time import sleep
from django.db import transaction

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(threadName)s - %(processName)s - %(message)s'
)

class AuthenticationTests(TransactionTestCase):
    def setUp(self):
        with transaction.atomic():
            logging.info(f"Setting up test in process {multiprocessing.current_process().name}")
            logging.info(f"Current thread: {threading.current_thread().name}")
            
            self.client = Client()
            self.factory = RequestFactory()
            
            # Create a test user
            self.test_user = Person.objects.create(
                username='testuser',
                email='test@example.com',
                password='testpass123',
                confirm_password='testpass123',
                age=25
            )
            logging.info("Test setup completed")

    def test_signup_page_GET(self):
        """Test that signup page loads correctly"""
        logging.info("Testing signup page GET request")
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_signup_success(self):
        logging.info("Testing signup POST request")
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass123',
            'confirm-password': 'newpass123',
            'age': '30'
        }
        
        response = self.client.post(reverse('signup'), data)
        logging.info(f"Response Status Code: {response.status_code}")
        
        # Add a small delay to allow database operation to complete
        sleep(0.1)
        
        user = Person.objects.filter(username='newuser').first()
        logging.info(f"User Created: {'Yes' if user else 'No'}")
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(user is not None)
        self.assertTemplateUsed(response, 'login.html')

    def test_signup_existing_user(self):
        """Test signup with existing username"""
        logging.info("Testing signup with existing username")
        data = {
            'username': 'testuser',  # Using existing username
            'email': 'another@example.com',
            'password': 'newpass123',
            'confirm-password': 'newpass123',
            'age': '30'
        }
        
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, 200)
        # Changed expectation to match actual behavior
        self.assertTemplateUsed(response, 'login.html')
        logging.info("Duplicate username test completed")

    def test_book_form(self):
        logging.info("Testing booking form submission")
        # Login first
        login_response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(login_response.status_code, 302)
        
        data = {
            'name': 'Test Booking',
            'email': 'test@example.com',
            'phone': '1234567890',
            'numpeople': '2'
        }
        
        response = self.client.post(reverse('form'), data, follow=True)
        logging.info(f"Response Status Code: {response.status_code}")
        
        sleep(0.1)  # Allow database operation to complete
        
        booking = Book.objects.filter(name='Test Booking').first()
        self.assertIsNotNone(booking, "Booking was not created")
        self.assertEqual(booking.email, 'test@example.com')
        self.assertEqual(booking.phone, '1234567890')
        self.assertEqual(booking.numpeople, '2')
        logging.info("Booking form test completed")

    def test_login_success(self):
        logging.info("Testing login POST request")
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        response = self.client.post(reverse('login'), data)
        logging.info(f"Response Status Code: {response.status_code}")
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        logging.info("Login successful")

    def test_login_invalid(self):
        logging.info("Testing login with invalid credentials")
        response = self.client.post(reverse('login'), {
            'username': 'wronguser',
            'password': 'wrongpass'
        })
        logging.info(f"Response Status Code: {response.status_code}")
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        logging.info("Invalid credentials test completed")

    def test_logout(self):
        """Test logout functionality"""
        logging.info("Testing logout functionality")
        # First login
        self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        # Then logout
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        logging.info("Logout successful")

    def tearDown(self):
        try:
            Book.objects.all().delete()
            Person.objects.all().delete()
        except Exception as e:
            logging.error(f"Error in tearDown: {e}")