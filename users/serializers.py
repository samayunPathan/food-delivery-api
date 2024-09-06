from rest_framework import serializers
from .models import User
from restaurants.serializers import RestaurantSerializer


class UserSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'restaurant']

        read_only_fields = ['id']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password',
                  'is_owner', 'is_employee', 'restaurant']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_owner=validated_data.get('is_owner', False),
            is_employee=validated_data.get('is_employee', False),
        )
        if 'restaurant' in validated_data:
            user.restaurant = validated_data['restaurant']
            user.save()
        return user
