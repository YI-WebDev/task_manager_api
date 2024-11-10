from datetime import datetime, timedelta
from rest_framework import serializers
from config.settings import USER_PASSWORD_EXPIRY_DAYS
from generics.serializer import HashIDModelSerializer
from . import models, exceptions

DATETIME_FORMAT = "%Y/%m/%d %H:%M:%S"


class UsersSerializer(HashIDModelSerializer):
    class Meta:
        model = models.User
        fields = (
            "id",
            "created_at",
            "username",
            "email",
            "password",
            "is_admin",
            "password_expiry_date",
            "is_password_expired",
        )
        read_only_fields = ("is_admin")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    username = serializers.CharField()
    created_at = serializers.DateTimeField(format=DATETIME_FORMAT, read_only=True)
    password_expiry_date = serializers.CharField(required=False)
    is_password_expired = serializers.SerializerMethodField()

    def get_is_password_expired(self, instance: models.User) -> bool:
        return bool(
            instance.password_expiry_date is not None
            and instance.password_expiry_date < datetime.now()
        )

    def validate_username(self, username):
        if models.User.objects.filter(username=username).exists():
            raise exceptions.UserNameAlreadyExists(username)
        return username

    def update(self, instance: models.User, validated_data):
        result = super().update(instance, validated_data)
        return result

    def create(self, validated_data):
        if USER_PASSWORD_EXPIRY_DAYS:
            validated_data["password_expiry_date"] = datetime.now() + timedelta(
                days=USER_PASSWORD_EXPIRY_DAYS
            )
        instance: models.User = super().create(validated_data)
        return instance
