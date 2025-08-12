from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login , logout , update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import AddUserForm
from .models import Profile



def home_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('login')

def register_view(request):
     if request.method == 'POST':
         form = UserCreationForm(request.POST)
         if form.is_valid():
             form.save()
             return redirect('/accounts/dashboard/')
         
     else:
        form = UserCreationForm()


     return render(request, 'accounts/register.html',{'form': form})
 
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect ('/accounts/dashboard')
        
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form':form})  


@login_required
def dashboard_view(request):
    profile = request.user.profile
    return render(request, 'accounts/dashboard.html', {'profile':profile})  

def logout_view(request):
     logout(request)
     return redirect('/accounts/login/')


@login_required 
def profile_view(request):
    profile = request.user.profile 

    if request.method == 'POST':
        user = request.user
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        profile_picture = request.FILES.get('profile_picture')
        
      
        user.username = new_username
        user.email = new_email
        user.save()
        
       
        if profile_picture:
            profile.profile_picture = profile_picture
            profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('profile')

    return render(request, 'accounts/profile.html', {'profile': profile})


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
        
    return render(request, 'accounts/change_password.html', {'form': form})      
 
    
     

@login_required
def add_user(request):
    if request.method == "POST":
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New user created successfully.")
            return redirect("dashboard")
    else:
        form = AddUserForm()
    return render(request, "accounts/add_user.html", {"form": form})

