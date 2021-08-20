
from .views import login, logout, register
from django.urls import path

urlpatterns = [
    # path('', homeview),
    path('login/', login),
    path('logout/', logout),
    path('register/', register),
]