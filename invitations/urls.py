"""
URL маршруты приглашения.
"""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.invitation_page),
    path('api/submit/', views.submit_invitation),
]
