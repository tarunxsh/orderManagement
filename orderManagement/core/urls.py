from django.urls import path
from .views import neworder , delivered,home

urlpatterns = [
    path('neworder/', neworder,name="neworder"),
    path('dlvr/', delivered,name="delivered"),  
    path('',home,name="home")  
]
