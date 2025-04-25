"""
URL configuration for project project.

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
from django.urls import path
from app.views import (
    home,
    load_stations, lines_list, line_form, line_stations,
    station_form, station_line,
    route_form, route_stations
)

urlpatterns = [
    path('', home, name='home'),
    path('stations/load/',     load_stations, name='load_stations'),
    path('lines/',             lines_list,    name='lines_list'),
    path('lines/query/',       line_form,     name='line_form'),
    path('lines/<int:pk>/',    line_stations, name='line_stations'),
    path('stations/query/',    station_form,  name='station_form'),
    path('stations/<int:pk>/', station_line,  name='station_line'),
    path('route/query/',       route_form,    name='route_form'),
    path('route/result/',      route_stations,name='route_stations'),
    path('admin/', admin.site.urls),
]
    