from rest_framework import serializers
from .models import Data, UserAuthority
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator


class UserAuthoritySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAuthority
        fields = ["user", "role"]


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
        error_messages={
            "required": "メールアドレスは必須項目です。",
            "invalid": "有効なメールアドレスを入力してください。",
        },
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        min_length=8,
        error_messages={
            "required": "パスワードは必須項目です。",
            "min_length": "パスワードは8文字以上にしてください。",
        },
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        label="Confirm Password",
        error_messages={
            "required": "パスワード確認は必須項目です。",
        },
    )
    role = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("id", "username", "password", "password2", "email", "role")
        extra_kwargs = {
            "username": {
                "required": True,
                "allow_blank": False,
                "min_length": 3,
                "max_length": 20,
                "validators": [
                    RegexValidator(
                        r"^[\w.@+-]+$",
                        "ユーザー名には英数字とアンダースコア(_)のみ使用できます。",
                        "invalid",
                    )
                ],
                "error_messages": {
                    "required": "ユーザー名は必須項目です。",
                    "min_length": "ユーザー名は3文字以上で入力してください。",
                    "max_length": "ユーザー名は20文字以下で入力してください。",
                },
            },
            "password": {
                "write_only": True,
                "required": True,
                "validators": [validate_password],
                "min_length": 8,
                "error_messages": {
                    "required": "パスワードは必須項目です。",
                    "min_length": "パスワードは8文字以上で入力してください。",
                },
            },
            "password2": {
                "write_only": True,
                "required": True,
                "error_messages": {
                    "required": "パスワード確認は必須項目です。",
                },
            },
            "role": {
                "write_only": True,
                "required": True,
                "error_messages": {
                    "required": "権限は必須項目です。",
                },
            },
        }

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate_password2(self, value):
        if self.initial_data["password"] != value:
            raise serializers.ValidationError(("パスワードが一致しません。"))
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("password2")
        role = validated_data.pop("role")
        username = validated_data.get('username')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': ['このユーザー名は既に使用されています。']})
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        UserAuthority.objects.create(user=user, role=role)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
