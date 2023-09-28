from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from .models import Course


@login_required
def order_form(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Handle form submission, e.g., save data to a database
            # You can access form.cleaned_data for each field
            # Return a success message
            return JsonResponse({'message': 'Order Confirmed'})
    else:
        form = OrderForm()

    return render(request, 'order_form.html', {'form': form})

def load_courses(request):
    department_id = request.GET.get('department')
    courses = Course.objects.filter(department_id=department_id).values('id', 'name')
    return JsonResponse(list(courses), safe=False)
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('registration:order_form')  # Redirect to the dashboard upon successful login
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('registration:login')

    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['password1']

        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    email=email
                )
                user.save()
                messages.success(request, 'Registration successful. Please log in.')
                return redirect('registration:login')  # Redirect to the login page after successful registration
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('registration:register')

    return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    return redirect('/') # Redirect to the login page after logout

