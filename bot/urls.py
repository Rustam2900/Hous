
from django.urls import path
from . import views

urlpatterns = [
    path('house_details/<int:id>/', views.house_details, name='house_details'),
]
