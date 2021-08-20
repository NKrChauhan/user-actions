from django.contrib import admin
from django.db import models
from .models import User
from .forms import UserAdminForm
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    model = User
    add_form = UserAdminForm
    form = UserAdminForm
    list_display = ['username', 'email', 'admin', 'last_login']
    search_fields = ['username', 'email']
    list_filter = ['admin', 'manager','client','employee', 'active']


admin.site.register(User, UserAdmin)