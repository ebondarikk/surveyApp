from django.db import models as orm
from rest_framework import permissions, viewsets, response, status

from . import models
from . import serializers


class Survey(viewsets.ModelViewSet):
    serializer_class = serializers.Survey

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        query = (
            orm.Q(is_active=True) if not self.request.user.is_authenticated else orm.Q()
        )
        return models.Survey.objects.filter(query)


class Question(viewsets.ModelViewSet):
    serializer_class = serializers.Question
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.Question.objects.all()


class SurveyProgress(viewsets.ModelViewSet):
    serializer_class = serializers.SurveyProgress

    list_serializer_class = serializers.SurveyProgressList

    filterset_fields = ("user_id",)

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        return self.serializer_class

    def get_queryset(self):
        queryset = models.SurveyProgress.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["survey"] = kwargs.get(self.lookup_field)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)
