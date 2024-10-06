from django.urls import path

from . import views
app_name = "charlist"
urlpatterns = [
    path("<slug:session_name>/<slug:char_name>/stats/", views.CharListStats.as_view(), name="CharListStats"),
    path("",views.SessionSelection.as_view(),name="SessionSelecion")
]