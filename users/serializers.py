from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta():
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'is_seller', 'date_joined']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class DetailUserSerializer(serializers.ModelSerializer):

    class Meta():
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'is_seller', 'date_joined']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UpdateStatusSerializer(serializers.ModelSerializer):

    class Meta():
        model = User
        fields = ['is_active']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
