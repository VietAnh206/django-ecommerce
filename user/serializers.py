from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from user.models import UserAccount


class UserAccountSerializer(UserCreateSerializer):
    """Dùng khi đăng ký (POST /users/)."""

    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta(UserCreateSerializer.Meta):
        model = UserAccount
        fields = ("id", "username", "email", "password", "first_name", "last_name", "phone", "address", "gender")


class UserProfileSerializer(serializers.ModelSerializer):
    """Dùng để đọc / cập nhật thông tin cá nhân (không có password)."""

    class Meta:
        model = UserAccount
        fields = ("id", "username", "email", "first_name", "last_name", "phone", "address", "gender")
        read_only_fields = ("id", "username")
