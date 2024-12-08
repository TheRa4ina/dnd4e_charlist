from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import path, reverse_lazy
from django.contrib.auth import views


app_name = "user"

urlpatterns = [
    path('login/', views.LoginView.as_view(template_name='auth/login.html'), name='login'), 
    path(
        'registration/', 
        CreateView.as_view(
            template_name='auth/registration.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('user:login'),
        ),
        name='registration',
    ),
    path('logout/', views.LogoutView.as_view(template_name='auth/logout.html'), name='logout'), 
]