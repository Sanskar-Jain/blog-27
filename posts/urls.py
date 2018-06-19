"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path

from .views import post_list, post_create, post_detail, post_update, post_delete

app_name = 'posts'

urlpatterns = [
	path('', post_list, name='list'),
    path('create', post_create, name='create'),
    path('<slug:slug>', post_detail, name='detail'),
    path('<slug:slug>/edit', post_update, name='update'),
    path('<slug:slug>/delete', post_delete, name='delete'),
]
