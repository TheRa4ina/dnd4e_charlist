from django.urls import path

from . import views

app_name = "user"

urlpatterns = [
    path("login/", views.login_page, name="login"),
    path("registration/", views.registration_page, name="registration"),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]