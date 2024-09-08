from rest_framework import serializers
from .models import User
from restaurants.serializers import RestaurantSerializer
from restaurants.models import Restaurant
from django.db import IntegrityError


class UserSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'restaurant']
        read_only_fields = ['id']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    restaurant = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(), required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password',
                  'is_owner', 'is_employee', 'restaurant']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print("Creating user with data:", validated_data)
        restaurant = validated_data.pop('restaurant', None)

        try:
            user = User(
                username=validated_data['username'],
                email=validated_data['email'],
                is_owner=validated_data.get('is_owner', False),
                is_employee=validated_data.get('is_employee', False),
            )
            if restaurant:
                user.restaurant = restaurant

            user.set_password(validated_data['password'])
            user.save()

            return user

        except IntegrityError as e:
            print(f"IntegrityError: {e}")
            raise serializers.ValidationError(f"Unable to create user: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise serializers.ValidationError(f"Unable to create user: {e}")
