from drf_yasg import openapi
from drf_yasg import renderers
from drf_yasg import views
from rest_framework import permissions

schema_view = views.get_schema_view(
    openapi.Info(
        title="SurveyApp API",
        default_version="v1",
        description="SurveyApp REST API documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

Json = schema_view.as_cached_view(
    0, None, renderer_classes=(renderers.SwaggerJSONRenderer,)
)

Swagger = schema_view.with_ui("swagger", cache_timeout=0)
