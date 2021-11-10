from django.urls import path, include

urlpatterns = [
    path("api/v1/content/", include("survey.urls")),
    path("api/v1/accounts/", include("accounts.urls")),
    path("api/v1/", include("apidoc.urls")),
]
