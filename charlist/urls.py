from django.urls import path

from . import views
app_name = "charlist"
urlpatterns = [
    path("<slug:session_name>/stats/", views.CharListStats.as_view(), name="CharListStats"),
    path("",views.SessionSelection.as_view(),name="SessionSelector"),
    path("<slug:session_name>/char_creator/",views.CharCreator.as_view(),name="CharCreator"),
    path("<slug:session_name>/add_char/",views.add_char,name="AddChar"),
    path("session_creator/",views.SessionCreator.as_view(),name="SessionCreator"),
    path("create_session/",views.add_session,name="AddSession"),
]