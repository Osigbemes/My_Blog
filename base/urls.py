from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    path('blog/<str:pk>/', views.blog, name="blog"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('create-blog/', views.createBlog, name="create-blog"),
    path('update-blog/<str:pk>/', views.updateBlog, name="update-blog"),
    path('delete-blog/<str:pk>/', views.deleteBlog, name="delete-blog"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    path('update-user/', views.updateUser, name="update-user"),

    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
]
