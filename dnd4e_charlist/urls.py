from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views

urlpatterns = [
    path('', include('charlist.urls')),
    path('admin/', admin.site.urls),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
