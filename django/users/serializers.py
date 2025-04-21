from project_service.utils import encrypt_id
from rest_framework import serializers

from django.contrib.auth.hashers import check_password, make_password

from .models.address import City, Country, State
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
    
class UserSerializer(serializers.ModelSerializer):
    cvid = serializers.SerializerMethodField()
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())

    class Meta:
        model = User
        fields = (
            'cvid',
            'first_name',
            'last_name',
            'email',
            'password',
            'phone',
            'city',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_cvid(self, obj):
        return encrypt_id(obj.id, obj._meta.db_table)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.password = make_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        for attr in ('first_name', 'last_name', 'email', 'phone', 'city'):
            if attr in validated_data:
                setattr(instance, attr, validated_data[attr])

        password = validated_data.get('password', None)
        if password:
            instance.password = make_password(password)

        instance.save()
        return instance


class CountrySerializer(serializers.ModelSerializer):
    cvid = serializers.SerializerMethodField()

    def get_cvid(self, obj):
        return encrypt_id(obj.id, obj._meta.db_table)
    
    class Meta:
        model = Country
        fields = ('cvid', 'name', 'code')


class StateSerializer(serializers.ModelSerializer):
    cvid = serializers.SerializerMethodField()
    country = CountrySerializer()  # Expande o país

    class Meta:
        model = State
        fields = ('cvid', 'name', 'acronym', 'country')

    def get_cvid(self, obj):
        return encrypt_id(obj.id, obj._meta.db_table)


class CitySerializer(serializers.ModelSerializer):
    cvid = serializers.SerializerMethodField()
    state = StateSerializer()

    class Meta:
        model = City
        fields = ('cvid', 'name', 'state')

    def get_cvid(self, obj):
        return encrypt_id(obj.id, obj._meta.db_table)