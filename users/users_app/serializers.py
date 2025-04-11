from django.contrib.auth.hashers import check_password, make_password
from rest_framework import serializers

from .models.user import User


class UserAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        try:
            user = User.objects.get(email=username) 
        except User.DoesNotExist:
            raise serializers.ValidationError("User not exist")

        if not check_password(password, user.password):
            raise serializers.ValidationError("Invalid credentials")

        data['user'] = user
        return data

class UserDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']
        
class UserSerializer(serializers.ModelSerializer):
    cvusertype = serializers.IntegerField()

    class Meta:
        model = User
        fields = ['id', 'name', 'email']

    def create(self, validated_data):
       
        user = User.objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
       
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        
        instance.save()
        return instance
