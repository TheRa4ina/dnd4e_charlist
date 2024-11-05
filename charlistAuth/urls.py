from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.login_page, name="login"),
    path("registration/", views.registration_page, name="registration"),
]