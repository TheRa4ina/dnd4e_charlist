from django.urls import path

from . import views

app_name = "charlist"

urlpatterns = [
    path(
        "session_creator/",
        views.SessionCreator.as_view(),
        name="SessionCreator"
    ),
    path("create_session/", views.add_session, name="AddSession"),
    path(
        "invite/<str:invitation_key>/",
        views.join_session,
        name="JoinSession"
    ),
    path("", views.SessionSelection.as_view(), name="SessionSelector"),
    path(
        "<int:session_id>/char_selector/",
        views.CharSelector.as_view(),
        name="CharSelector"
    ),
    path(
        "<int:session_id>/char_creator/",
        views.CharCreator.as_view(),
        name="CharCreator"),
    path("<int:session_id>/add_char/", views.add_char, name="AddChar"),
    path(
        "<int:session_id>/<int:char_id>/stats/",
        views.CharListStats.as_view(),
        name="CharListStats"
    ),
    path(
        'save_model_form_data/<slug:model_form_name>/',
        views.save_model_form_data,
        name='save_model_form_data'
    ),
    path(
        'save_handwritten_form_data/<str:model_form_name>/',
        views.save_handwritten_form_data,
        name='save_handwritten_form_data'
    ),
    path(
        'save_selected_skills/',
        views.save_selected_skills,
        name='save_selected_skills'
    ),
        path(
        'long_poll/<int:char_id>/',
        views.long_poll,
        name='long_poll'
    ),
]
