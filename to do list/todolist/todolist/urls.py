"""
URL configuration for todolist project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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


from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include
from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('urgent/', urgent, name='urgent'),
    path('personal/', personal, name='personal'),
    path('work/', work, name='work'),
    path('delete/<int:id>/', delete_task, name='delete_task'),  # task_id passed here
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('i18n/', include('django.conf.urls.i18n')),
]