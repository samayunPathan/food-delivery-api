from rest_framework import serializers
from .models import User
from restaurants.serializers import RestaurantSerializer


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    Includes the restaurant field, which is a nested serializer for the Restaurant model.
    """
    restaurant = RestaurantSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_owner', 'is_employee', 'restaurant']
        read_only_fields = ['id']


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_owner', 'is_employee', 'restaurant']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_owner=validated_data['is_owner'],
            is_employee=validated_data['is_employee'],
            restaurant=validated_data['restaurant']
        )
        return user