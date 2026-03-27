from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required 
from .models import *
from .forms import *
from django.utils import timezone
from datetime import timedelta



@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        new_username = request.POST.get('username')

        user = request.user
        
        # 1. Username Validation Check
        # Check karein ki username input aaya hai aur current username se alag hai
        if new_username and new_username != user.username:
            # Check karein ki kya ye new_username pehle se database mein kisi aur ka hai
            if User.objects.filter(username=new_username).exists():
                messages.error(request, 'Yeh username pehle se taken hai. Kripya koi aur username chunein.')
                return redirect('profile') # 'profile' string use karein (urls.py ka name)
            else:
                user.username = new_username # Agar taken nahi hai, tabhi update karein

        # 2. Baki details update karein
        user.first_name = first_name
        user.last_name = last_name
        
        # 3. Save karein aur success message dein
        try:
            user.save()
            messages.success(request, 'Your profile has been updated successfully!')
        except Exception as e:
            messages.error(request, f'Kuch galat ho gaya: {e}')
            
        return redirect('profile') 
        
    return render(request, 'account/profile.html')