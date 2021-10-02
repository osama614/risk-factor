
from django.urls import path
from .views import Diagnose


app_name = "diagnostic"
urlpatterns = [
    path('', Diagnose.as_view()),
    
   
]