from django.contrib.auth import login, logout
from rest_framework import views, response, viewsets

from . import serializers


class Login(viewsets.GenericViewSet):
    serializer_class = serializers.Login

    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return response.Response()


class Logout(views.APIView):
    def post(self, request):
        logout(request)
        return response.Response()
