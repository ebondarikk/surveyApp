from django.contrib.auth import authenticate
from rest_framework import serializers


class Login(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(username=attrs["username"], password=attrs["password"])

        if not user:
            raise serializers.ValidationError("Incorrect email or password.")

        if not user.is_active:
            raise serializers.ValidationError("User is disabled.")

        return {"user": user}

    class Meta:
        fields = ("username", "password")
