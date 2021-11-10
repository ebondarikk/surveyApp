from django.urls import path

from . import views

urlpatterns = [
    path("surveys/", views.Survey.as_view({"post": "create", "get": "list"})),
    path(
        "surveys/<int:pk>/",
        views.Survey.as_view({"put": "update", "delete": "destroy", "get": "retrieve"}),
    ),
    path("surveys/<int:pk>/pass/", views.SurveyProgress.as_view({"post": "create"})),
    path("surveys/passed/", views.SurveyProgress.as_view({"get": "list"})),
    path("questions/", views.Question.as_view({"post": "create", "get": "list"})),
    path(
        "questions/<int:pk>/",
        views.Question.as_view(
            {"put": "update", "delete": "destroy", "get": "retrieve"}
        ),
    ),
]
