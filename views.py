from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import *
from .models import *
from django.db.models import Q

from django.http import JsonResponse
from django.conf import settings
import os

import joblib
import numpy as np

def base(request):
    return render(request, 'base.html')

def about(request):
    return render(request, 'about/about.html')

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            #create a new registration object and avoid saving it yet
            new_user = user_form.save(commit=False)
            #reset the choosen password
            new_user.set_password(user_form.cleaned_data['password'])
            #save the new registration
            new_user.save()
            return render(request, 'registration/register_done.html',{'new_user':new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html',{'user_form':user_form})

def profile(request):
    return render(request, 'profile/profile.html')



@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = EditProfileForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
    else:
        user_form = EditProfileForm(instance=request.user)
    
    return render(request, 'profile/edit_profile.html', {'user_form': user_form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, 'Your account was successfully deleted.')
        return redirect('base')  # Redirect to the homepage or another page after deletion

    return render(request, 'registration/delete_account.html')
# das
@login_required
def dashboard(request):
    users_count = User.objects.all().count()
    consumers = Consumer.objects.all().count
    notify_users = Notification.objects.all().count()
    review_count = Review.objects.all().count()

    context = {
        'users_count':users_count,
        'consumers':consumers,
        'notify_users':notify_users,
        'review_count':review_count,
        'barData': [10, 20, 30],
        'lineData': [30, 25, 35],
        'pieData': [10, 40, 50],
        'scatterData': [{'x': 10, 'y': 20}, {'x': 15, 'y': 10}, {'x': 20, 'y': 30}],
        
    }
    return render(request, "dashboard/dashboard_crop.html", context=context)
#CRUD operations start here
@login_required
def dashvalues(request):
    consumers = Consumer.objects.all()
    search_query = ""
    
    if request.method == "POST": 
        if "create" in request.POST:
            name = request.POST.get("name")
            email = request.POST.get("email")
            image = request.FILES.get("image")
            content = request.POST.get("content")

            Consumer.objects.create(
                name=name,
                email=email,
                image=image,
                content=content
            )
            messages.success(request, "Consumer added successfully")
    
        elif "update" in request.POST:
            id = request.POST.get("id")
            name = request.POST.get("name")
            email = request.POST.get("email")
            image = request.FILES.get("image")
            content = request.POST.get("content")

            consumer = get_object_or_404(Consumer, id=id)
            consumer.name = name
            consumer.email = email
            consumer.image = image
            consumer.content = content
            consumer.save()
            messages.success(request, "Consumer updated successfully")
    
        elif "delete" in request.POST:
            id = request.POST.get("id")
            Consumer.objects.get(id=id).delete()
            messages.success(request, "Consumer deleted successfully")
        
        elif "search" in request.POST:
            search_query = request.POST.get("query")
            consumers = Consumer.objects.filter(Q(name__icontains=search_query) | Q(email__icontains=search_query))

    context = {
        "consumers": consumers, 
        "search_query": search_query
    }
    return render(request, "crud/dashvalue.html", context=context)
# CRUD operations end here

# Contact start
@login_required
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for contacting us!")
            return redirect('dashboard')  # Redirect to the same page to show the modal
    else:
        form = ContactForm()

    return render(request, 'contact/contact_form.html', {'form': form})

# contact end

# review start
def add_review(request, consumer_id):
    consumer = get_object_or_404(Consumer, id=consumer_id)
    consumer_name = consumer.name

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Assuming you have a Review model with fields 'comment' and 'rating'
            review = form.save(commit=False)
            review.consumer = consumer
            review.save()
            # You may want to add a success message here
            return redirect('dashboard')  # Redirect to the dashboard or any other page
    else:
        form = ReviewForm()

    return render(request, 'review/review.html', {'consumer_id': consumer_id, 'consumer_name': consumer_name, 'form': form})
# review end

# views.py


def view_reviews(request, consumer_id):
    consumer = get_object_or_404(Consumer, id=consumer_id)
    reviews = Review.objects.filter(consumer=consumer)

    return render(request, 'review/view_reviews.html', {'consumer': consumer, 'reviews': reviews})

#notification

@login_required
def user_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notification/user_notifications.html', {'notifications': notifications})


import smtplib
from email.message import EmailMessage

from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages

@login_required
def send_email(request):
    if request.method == 'POST':
        receiver = request.POST.get('receiver')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[receiver],
        )
        try:
            email.send()
            messages.success(request, 'Email sent successfully!')
        except:
            messages.error(request, 'Failed to send email.')

        return redirect('send_email')

    return render(request, 'email/sendemail.html')


@login_required
def chat(request):
    return render(request, 'chat/chat.html')

# 
# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import PhoneInfo
from .forms import PhoneInfoForm

def phone_book(request):
    contacts = PhoneInfo.objects.all()
    return render(request, 'phone/phone_book.html', {'contacts': contacts})

def add_contact(request):
    if request.method == 'POST':
        form = PhoneInfoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('phone_book')
    else:
        form = PhoneInfoForm()
    return render(request, 'phone/add_contact.html', {'form': form})

def edit_contact(request, pk):
    contact = get_object_or_404(PhoneInfo, pk=pk)
    if request.method == 'POST':
        form = PhoneInfoForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('phone_book')
    else:
        form = PhoneInfoForm(instance=contact)
    return render(request, 'phone/edit_contact.html', {'form': form})

def delete_contact(request, pk):
    contact = get_object_or_404(PhoneInfo, pk=pk)
    if request.method == 'POST':
        contact.delete()
        return redirect('phone_book')
    return render(request, 'phone/delete_contact.html', {'contact': contact})


# alarm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Alarm
from .forms import AlarmForm

from django.shortcuts import render, redirect
from .forms import AlarmForm

from django.contrib.auth.models import User  # Import User model if not already imported

def create_alarm(request):
    if request.method == 'POST':
        form = AlarmForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('alarm_list')  
    else:
        form = AlarmForm()
    
    users = User.objects.all()  
    return render(request, 'alarm/create_alarm.html', {'form': form, 'users': users})

def alarm_list(request):
    alarms = Alarm.objects.all()
    return render(request, 'alarm/alarm_list.html', {'alarms': alarms})

def edit_alarm(request, pk):
    alarm = get_object_or_404(Alarm, pk=pk)
    if request.method == 'POST':
        form = AlarmForm(request.POST, instance=alarm)
        if form.is_valid():
            form.save()
            return redirect('alarm_list')
    else:
        form = AlarmForm(instance=alarm)
    return render(request, 'alarm/edit_alarm.html', {'form': form})

def delete_alarm(request, pk):
    alarm = get_object_or_404(Alarm, pk=pk)
    if request.method == 'POST':
        alarm.delete()
        return redirect('alarm_list')
    return render(request, 'alarm/delete_alarm.html', {'alarm': alarm})

from datetime import datetime

def check_alarm1(request):
    if request.method == "GET":
        user1 = request.user.username
        print(user1) 
        alarm_exists = Alarm.objects.filter(user=user1).exists()
        print(alarm_exists)
        return render(request, 'alarm/alarm.html', {'alarm': alarm_exists})


def check_alarm(request):
    if request.method == "GET":
        current_time = datetime.now().strftime('%H:%M')  # Format to HH:MM
        user1 = request.user.username
        alarm_exists = Alarm.objects.filter(time=current_time, user=user1).exists()
        if alarm_exists == None:
            alarm = None
        else:
            alarm = "play"
        return render(request, 'alarm/alarm.html', {'alarm': alarm,'current_time':current_time,'alarm_exists':alarm_exists})
    
import geocoder

from geopy.geocoders import Nominatim

def get_city_name(lat, long):
    # Initialize the geolocator
    geolocator = Nominatim(user_agent="geoapiExercises")

    # Reverse geocode the coordinates
    location = geolocator.reverse((lat, long), language='en')

    # Extract the city name from the address
    city = location.raw['address']

    return city


def local(request):
    lat = 16.4292 # Example latitude
    long = 74.5879 # Example longitude

    # city_name = get_city_name(lat, long)
    return render(request, 'location/location.html',{'lat':lat,'long':long})