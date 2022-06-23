from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    """  
    serializer for user's account
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'bio', 'avatar', 'followers', 'dob', 'following']

    def update(self, instance, validated_data):
        # bulk update the only fields that are supplied (to improve performance)
        # using the key
        for key in validated_data.keys():
            setattr(instance, key, validated_data[key])
        instance.save()
        return instance

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only = True)
    username = serializers.CharField(min_length=3)
    class Meta:
        model = User
        fields = ['username', 'password']

    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']
        user = authenticate(username=username, password=password)
        if user is None or not user.is_active:
            raise serializers.ValidationError("Invalid Credentials or details")
        return super().validate(attrs)

    def save(self):
        """ output token pair for user"""
        username = self.validated_data['username']
        password = self.validated_data['password']
        user = authenticate(username=username, password=password)
        return user.get_tokens()

class RegisterSerializer(serializers.ModelSerializer):
    """
        serializer for user registration
    """
    password = serializers.CharField(min_length=6, write_only = True)
    password2 = serializers.CharField(min_length=6, write_only = True)
    class Meta:
        model = User
        fields = ['username', 'password', 'password2']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Password must match")
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)

    