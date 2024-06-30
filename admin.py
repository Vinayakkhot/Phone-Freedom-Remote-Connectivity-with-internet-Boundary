from .models import *
from django import forms
from django.contrib import admin
from .models import Notification
from .forms import NotificationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "message"]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["id", "consumer", "comment", "rating"]
