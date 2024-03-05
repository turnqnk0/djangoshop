from django.contrib import admin
from django.contrib.sessions.models import Session
from .models import UserProfile, Address
# Register your models here.


admin.site.register(Session)
admin.site.register(UserProfile)
admin.site.register(Address)

