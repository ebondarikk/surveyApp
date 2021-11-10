from django import urls

from . import views

urlpatterns = (
    urls.re_path(r"docs/?$", views.Swagger, name="schema-swagger-ui"),
    # urls.re_path(r"$", views.Json, name="schema-json"),
)
