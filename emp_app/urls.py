"""
URL configuration for office_emp_proj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path,include
from .import views
from .views import admin_login, admin_dashboard, admin_logout

urlpatterns = [
    
    path('',views.index, name='index.html'),
    path("admin_login/", views.admin_login, name="admin_login"),
    path("admin_dashboard/", views.admin_dashboard, name="admin_dashboard"), 
    path('addEmp/',views.addEmp, name='addEmp'),
    path('removeEmp/',views.removeEmp, name='removeEmp'),
    path('filterEmp/',views.filterEmp, name='filterEmp'),
    path('viewEmp/',views.viewEmp, name='viewEmp'),
]
