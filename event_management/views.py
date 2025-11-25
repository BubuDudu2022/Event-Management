from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from events.models import EventCategory, Event
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import JsonResponse


def user_home(request):
    return render(request, 'events/user_event_list.html')

def register_page(request):
    return HttpResponse("Registration coming soon")

def user_logout(request):
    logout(request)
    return redirect("user-category-list") 

def ajax_login(request):
    if request.method == "POST":
        if request.headers.get("X-Requested-With") != "XMLHttpRequest":
            return JsonResponse({"status": "error", "message": "Invalid access"}, status=400)

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        next_url = request.POST.get("next", "/")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({"status": "success", "redirect": next_url})

        return JsonResponse({"status": "error", "message": "Invalid credentials"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


def ajax_register(request):
    if request.method == "POST":
        if request.headers.get("X-Requested-With") != "XMLHttpRequest":
            return JsonResponse({"status": "error", "message": "Invalid access"}, status=400)

        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password1", "")
        next_url = request.POST.get("next", "/")

        if User.objects.filter(username=email).exists():
            return JsonResponse({"status": "error", "message": "Email already exists"}, status=400)

        if not password:
            return JsonResponse({"status": "error", "message": "Password is required"}, status=400)

        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = name
        user.save()

        login(request, user)

        return JsonResponse({"status": "success", "redirect": next_url})

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


@login_required(login_url='login')
def dashboard(request):
    user = User.objects.count()
    event_ctg = EventCategory.objects.count()
    event = Event.objects.count()
    complete_event = Event.objects.filter(status='completed').count()
    events = Event.objects.all()
    context = {
        'user': user,
        'event_ctg': event_ctg,
        'event': event,
        'complete_event': complete_event,
        'events': events
    }
    return render(request, 'dashboard.html', context)

def login_page(request):
    forms = LoginForm()
    if request.method == 'POST':
        forms = LoginForm(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
    context = {
        'form': forms
    }
    return render(request, 'login.html', context)

def logut_page(request):
    logout(request)
    return redirect('login')