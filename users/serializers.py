from rest_framework import serializers
from .models import CustomUser, Profile
from django.contrib.auth import authenticate
import os
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password', 'confirm_password']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            role=validated_data.get('role', CustomUser.Roles.JOB_SEEKER)
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")

class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['user', 'profile_completed'] # Prevent manual changes

    def validate_resume(self, value):
        if value.size > 2 * 1024 * 1024:  # 2 MB limit
            raise serializers.ValidationError("Resume file too large (max 2MB).")
        ext = os.path.splitext(value.name)[1].lower()
        if ext not in ['.pdf', '.doc', '.docx']:
            raise serializers.ValidationError("Unsupported file type. Use PDF or DOC.")
        return value

    def validate_profile_picture(self, value):
        if value.size > 2 * 1024 * 1024:  # 2 MB limit
            raise serializers.ValidationError("Image too large (max 2MB).")
        return value

    def update(self, instance, validated_data):
        # Extract user fields
        user_data = validated_data.pop('user', {})
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        # Update profile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.profile_completed = all(
            getattr(instance, field) for field in ['country', 'phone_number', 'gender']
        )
        instance.save()

        return instance