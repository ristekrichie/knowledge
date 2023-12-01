from django.urls import path

from .views import base_view

app_name='theme'

urlpatterns = [
    path('', base_view, name='base_view'),
]