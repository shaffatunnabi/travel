from django.shortcuts import render, redirect
from Travel.models import Person, Book

def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Retrieve the user by username.
            person = Person.objects.get(password=password)

            # Use `check_password` to verify the hashed password.
            if password==person.password:
                # Redirect to a home page or dashboard after successful login.
                return render(request, 'index.html')  # Replace 'home' with your target page name.
            else:
                # Password is incorrect.
                return render(request, 'login.html', {'message': 'Incorrect password.'})
        except Person.DoesNotExist:
            # User does not exist.
            return render(request, 'login.html', {'message': 'User does not exist.'})

    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        age = request.POST.get('age')
        person=Person(username=username, email=email, password=password, confirm_password=confirm_password, age=age)
        person.save()
    
    return render(request, 'signup.html')

def form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        numpeople = request.POST.get('numpeople')
        book=Book(name=name, email=email, phone=phone, numpeople=numpeople)
        book.save()
    return render(request, 'form.html', {'message': 'Submit Successful.'})