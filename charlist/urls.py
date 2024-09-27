from django.urls import path

from . import views

urlpatterns = [
    path("charlist", views.CharListStats.as_view(), name="CharListStats"),
]