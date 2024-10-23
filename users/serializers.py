from rest_framework import serializers
from .models import CustomUser  # Import CustomUser instead


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True) 
    class Meta:
        model = CustomUser  # Use CustomUser here
        fields = ('id', 'username', 'email', 'password', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(**validated_data)  # Use CustomUser here
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct.")
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("New password and confirmation do not match.")
        return attrs

    def validate_new_password(self, value):
        if len(value) < 8:  # Example validation
            raise serializers.ValidationError("New password must be at least 8 characters long.")
        return value