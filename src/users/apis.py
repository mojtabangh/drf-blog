from django.core.validators import MinLengthValidator, MaxLengthValidator
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .models import User
from .services import create_user


class UserRegisterApi(APIView):
    class InputUserRegisterSerializer(serializers.Serializer):
        email = serializers.EmailField(required=True,)
        password = serializers.CharField(
            required=True,
            validators=[
                MinLengthValidator(limit_value=10),
                MaxLengthValidator(limit_value=32),
            ],
        )
        confirm_password = serializers.CharField(required=True,)

        def validate(self, data):
            if not data.get("password") or not data.get("confirm_password"):
                raise serializers.ValidationError("You must enter password and confirm password")

            if data.get("password") != data.get("confirm_password"):
                raise serializers.ValidationError("Password and confirm password are not the same.")

            return data

    class OutputUserRegisterSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ("email", "created_at", "updated_at")

    @extend_schema(request=InputUserRegisterSerializer, responses=OutputUserRegisterSerializer)
    def post(self, request):
        data = self.InputUserRegisterSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        try:
            user = create_user(
                email=data.validated_data("email"),
                password=data.validated_data("password"),
                is_active=True
            )
            return user

        except Exception as ex:
            return Response(
                f"{ex}",
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            self.OutputUserRegisterSerializer(user),
            status=status.HTTP_201_CREATED
        )
