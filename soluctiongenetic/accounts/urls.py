from django.urls import path

from .views import singup
from .views import logouter
from .views import loginx
urlpatterns = [
    path('singup', singup, name='singup'),
    path('logout',logouter, name="logout"),
    path('login', loginx,name="loginx"),
    path('', loginx,name="loginx"),
    
]
