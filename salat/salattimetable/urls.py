from django.urls import path
from . import views

urlpatterns = [
    # Example route for the home page
    path('', views.home, name='home'),
]