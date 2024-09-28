from django.urls import path

from . import views

urlpatterns = [
    path("", views.CharListStats.as_view(), name="CharListStats"),
]