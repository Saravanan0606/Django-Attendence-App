from django.utils import timezone
from datetime import date
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
import requests

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
def landing_page(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        within_perimeter = request.POST.get('withinPerimeter')

        current_date = timezone.now().date()

        existing_attendance = Attendance.objects.filter(user=request.user, created_at__date=current_date).first()

        if existing_attendance:
            return JsonResponse({"error": "Attendance already recorded for today."})

        if within_perimeter == 'true':
            attendance_present = Attendance.objects.create(user=request.user, latitude=latitude, longitude=longitude, is_present=True)
            attendance_present.save()
            return JsonResponse({"message": "Attendance recorded successfully!"})
        else:
            attendance_absent = Attendance.objects.create(user=request.user, latitude=latitude, longitude=longitude, is_present=False)
            attendance_absent.save()
            return JsonResponse({"error": "You are not within the permitted perimeter to mark attendance."})

    attendances = Attendance.objects.filter(user=request.user)
    user_details = UserProfile.objects.get(user=request.user)
    emp_num = user_details.emp_num

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        attendances_list = [
            {
                "emp_num": emp_num,
                "is_present": attendance.is_present,
                "created_at": attendance.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for attendance in attendances
        ]
        return JsonResponse({"attendances": attendances_list})

    context = {
        'attendances': attendances,
        'emp_num': emp_num,
    }

    return render(request, 'accounts/landing.html', context)

@login_required(login_url='login')
def view_attendence(request):
    # Retrieve attendance records from the database
    attendences = Attendance.objects.filter(user=request.user)
    user_details = UserProfile.objects.get(user=request.user)
    emp_num = user_details.emp_num
    context = {
        'attendences': attendences,
        'emp_num': emp_num,
    }
    
    return render(request, 'accounts/landing.html', context)

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, "You are logged Out!")
    return redirect('login')