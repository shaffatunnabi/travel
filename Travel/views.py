from django.shortcuts import render, redirect, HttpResponse
from Travel.models import Person, Book
from .utils import DatabaseThread, save_person_thread, save_booking_thread, send_email_thread
from django.http import JsonResponse
import logging
import threading
import concurrent.futures
from datetime import datetime
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(threadName)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Thread pool executor for managing concurrent tasks
thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=3)

def index(request):
    # Pass session data to template
    context = {
        'is_authenticated': request.session.get('is_authenticated', False),
        'username': request.session.get('username', '')
    }
    
    if request.method == 'GET':
        search = request.GET.get('search')
        if search:
            try:
                future = thread_pool.submit(perform_search, search)
                result = future.result(timeout=2.0)
                return JsonResponse(result)
            except concurrent.futures.TimeoutError:
                return JsonResponse({'status': 'processing'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})
    return render(request, 'index.html', context)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            person = Person.objects.get(password=password)
            if password == person.password:
                # Set session variables
                request.session['user_id'] = person.id
                request.session['username'] = person.username
                request.session['is_authenticated'] = True
                
                # Set session to expire when browser closes
                request.session.set_expiry(0)
                
                return redirect('index')
            else:
                return render(request, 'login.html', {'message': 'Incorrect password.'})
        except Person.DoesNotExist:
            return render(request, 'login.html', {'message': 'User does not exist.'})

    return render(request, 'login.html')

def logout_view(request):
    # Clear all session data
    request.session.flush()
    # Redirect to home page
    return redirect('index')

def signup(request):
    if request.method == 'POST':
        user_data = {
            'username': request.POST.get('username'),
            'email': request.POST.get('email'),
            'password': request.POST.get('password'),
            'confirm_password': request.POST.get('confirm-password'),
            'age': request.POST.get('age')
        }
        
        logger.info(f"Signup initiated for user: {user_data['username']}")
        try:
            # Submit registration to thread pool
            future = thread_pool.submit(save_person_thread, **user_data)
            future.result(timeout=3.0)  # Wait for completion with timeout
            
            logger.info(f"Signup successful for user: {user_data['username']}")
            return render(request, 'login.html')
        except Exception as e:
            logger.error(f"Signup error: {str(e)}")
            return render(request, 'signup.html', {'error': str(e)})
    
    return render(request, 'signup.html')

def form(request):
    # Check if user is logged in
    if not request.session.get('is_authenticated'):
        return redirect('login')
    
    # Get user data from session
    try:
        user = Person.objects.get(id=request.session.get('user_id'))
        initial_data = {
            'name': user.username,
            'email': user.email,
        }
    except Person.DoesNotExist:
        initial_data = {}
    
    if request.method == 'POST':
        booking_data = {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'numpeople': request.POST.get('numpeople'),
            'user_id': request.session.get('user_id')  # Add user_id to booking
        }
        return render(request, 'index.html')
    
        # Server-side validation
        errors = {}
        
        # Name validation
        if not re.match(r'^[A-Za-z ]{2,50}$', booking_data['name']):
            errors['name'] = 'Name should only contain letters and be 2-50 characters long'
            
        # Email validation
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', booking_data['email']):
            errors['email'] = 'Please enter a valid email address'
            
        # Phone validation
        if not re.match(r'^[0-9]{10}$', booking_data['phone']):
            errors['phone'] = 'Please enter a valid 10-digit phone number'
            
        # Number of people validation
        try:
            num_people = int(booking_data['numpeople'])
            if num_people < 1 or num_people > 10:
                errors['numpeople'] = 'Number of people must be between 1 and 10'
        except ValueError:
            errors['numpeople'] = 'Please enter a valid number'

        if errors:
            return JsonResponse({
                'status': 'error',
                'errors': errors
            })
        
        try:
            # Add user reference to booking data
            booking_data['user'] = user
            booking_future = thread_pool.submit(save_booking_thread, **booking_data)
            email_future = thread_pool.submit(
                send_email_thread,
                to_email=booking_data['email'],
                subject="Booking Confirmation"
            )
            
            booking_result = booking_future.result(timeout=3.0)
            
            # Send WebSocket notification
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "booking_updates",
                {
                    "type": "booking_update",
                    "message": {
                        "status": "confirmed",
                        "booking_id": booking_result.id,
                        "message": f"New booking confirmed for {booking_data['name']}"
                    }
                }
            )
            
            return JsonResponse({
                'message': 'Your booking has been confirmed.',
                'status': 'success'
            })
            
        except Exception as e:
            return JsonResponse({
                'message': 'An error occurred during booking.',
                'status': 'error'
            })
    
    return render(request, 'form.html', {'initial_data': initial_data})

# Helper functions
def authenticate_user(username, password):
    try:
        person = Person.objects.get(password=password)
        if password == person.password:
            return {'success': True}
        return {'success': False, 'message': 'Incorrect password.'}
    except Person.DoesNotExist:
        return {'success': False, 'message': 'User does not exist.'}

def perform_search(query):
    # Implement your search logic here
    logger.info(f"Performing search for: {query}")
    # Add your search implementation
    return {'results': []}