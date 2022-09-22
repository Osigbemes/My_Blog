from django.urls import path
from . import views

urlpatterns = [
    path('',  views.getRoutes),
    path('blogs/', views.getBlogs),
    path('blogs/<str:pk>/', views.getBlog),
]
