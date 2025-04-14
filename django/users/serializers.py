from rest_framework import serializers

from django.contrib.auth.hashers import check_password, make_password

from .models.user import User
from .utils import encrypt_id


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
    
class UserSerializer(serializers.ModelSerializer):
    cvid = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'cvid',
            'first_name',
            'last_name',
            'email',
            'password',
            'phone'
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_cvid(self, obj):
        return encrypt_id(obj.id, obj._meta.db_table)
    
    def create(self, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)

        if 'password' in validated_data:
            instance.password = make_password(validated_data['password'])
        
        instance.save()
        return instance


