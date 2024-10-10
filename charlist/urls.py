from django.urls import path

from . import views
app_name = "charlist"
urlpatterns = [
    path("session_creator/",views.SessionCreator.as_view(),name="SessionCreator"),
    path("create_session/",views.add_session,name="AddSession"),
    path("",views.SessionSelection.as_view(),name="SessionSelector"),
    path("<int:session_id>/char_selector",views.CharSelector.as_view(),name="CharSelector"),
    path("<int:session_id>/char_creator/",views.CharCreator.as_view(),name="CharCreator"),
    path("<int:session_id>/add_char/",views.add_char,name="AddChar"),
    path("<int:session_id>/<slug:char_name>/stats/", views.CharListStats.as_view(), name="CharListStats"),
]