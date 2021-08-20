from .models import User
from django import forms


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password',
                   'active', 'admin','manager', 'employee','client']