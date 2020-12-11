from django.urls import path
from .views import neworder , delivered

urlpatterns = [
    path('neworder/', neworder,name="neworder"),
    path('dlvr/', delivered,name="delivered"),    
]
