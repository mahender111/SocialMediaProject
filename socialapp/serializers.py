from rest_framework import serializers
from .models import FriendRequest, Friendship
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Serializer for User 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email'] 


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            print('user',user)
            if user is None:
                print('yyyy')
                raise serializers.ValidationError("Invalid credentials, please try again.")
        else:
            print('gggg')
            raise serializers.ValidationError("Must include 'username' and 'password'.")

        data['user'] = user
        print('data',data)
        return data

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'timestamp', 'status']
        read_only_fields = ['sender', 'status']

class FriendRequestAcceptRejectSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'timestamp', 'status']
        read_only_fields = ['sender', 'receiver', 'timestamp']
    
class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ['id', 'user1', 'user2', 'created_at']



class LogoutSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
    