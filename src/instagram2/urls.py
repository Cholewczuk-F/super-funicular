"""instagram2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from profiles.views import (
    register, 
    login, 
    testing, 
    profile_detail_view,
    create_profile_follow)
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register),
    path('', include('django.contrib.auth.urls')),
    path('', testing),
    path('profiles/<int:id>/', profile_detail_view, name='profile-detail'),
    path('profiles/follow/<int:user_id>/', create_profile_follow)
]
