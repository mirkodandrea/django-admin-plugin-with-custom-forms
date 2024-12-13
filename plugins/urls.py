from django.urls import path
from . import views

urlpatterns = [
    path('dynamic_form/<str:plugin_name>/', views.dynamic_form, name='dynamic_form'),
]
