from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
import requests
from geopy.distance import geodesic

from accounts.models import Attendance, UserProfile

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
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        within_perimeter = request.POST.get('withinPerimeter')  # Get the withinPerimeter status from the POST data
        print(latitude, longitude)

        if within_perimeter == 'true':  # Check if withinPerimeter is 'true' (string)
            # Record attendance if the user is within the permitted perimeter
            attendance_present = Attendance.objects.create(user=request.user, latitude=latitude, longitude=longitude, is_present=True)
            attendance_present.save()
            return JsonResponse({"message": "Attendance recorded successfully!"})  # Wrap the message inside a dictionary
        else:
            attendance_absent = Attendance.objects.create(user=request.user, latitude=latitude, longitude=longitude, is_present=False)
            attendance_absent.save()
            # Do something else (e.g., display a message, log the event) if the user is not within the permitted perimeter
            return JsonResponse({"error": "User is not within the attendence perimeter."})  
    else:
        return JsonResponse({"error": "Error: POST request required."})  

@login_required(login_url='login')
def view_attendance(request):
    # Fetch attendance data for the logged-in user
    attendances = Attendance.objects.filter(user=request.user)
    data = serialize('json', attendances)

    return JsonResponse(data, safe=False)

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, "You are logged Out!")
    return redirect('login')