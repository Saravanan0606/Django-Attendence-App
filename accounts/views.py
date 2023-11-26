from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
import requests

from accounts.models import UserProfile

# Create your views here.

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(request, email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in!!")
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('attendence')
        else:
            messages.error(request, 'Invalid Email or Password')
            return render(request, 'accounts/login.html')
        
    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def attendence(request):
    details = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'details': details,
    }
    return render(request, 'accounts/landing.html', context)

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

@login_required(login_url='login')
def record_attendance(request):
    if request.method == 'POST':
        # Get latitude and longitude from POST data
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        print(latitude, longitude)

        # Your logic to check if the location is within the specified area
        # Perform necessary checks, validations, and record attendance in your database

        # Example response (modify as needed)
        return JsonResponse({'message': 'Attendance recorded successfully!'})

    # If request method is not POST or other error handling
    return JsonResponse({'error': 'Invalid request'})

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, "You are logged Out!")
    return redirect('login')