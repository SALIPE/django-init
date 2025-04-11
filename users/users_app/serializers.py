from django.contrib.auth.hashers import check_password, make_password
from rest_framework import serializers

from .models import Tbuser, Tbusertype


class UserAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        try:
            user = Tbuser.objects.get(ccemail=username) 
        except Tbuser.DoesNotExist:
            # Raise an error if the user does not exist
            raise serializers.ValidationError("User not exist")

        # Check if the provided password matches the hashed password in the database
        if not check_password(password, user.ccpassword):
            raise serializers.ValidationError("Invalid credentials")

        # If valid, add the user instance to validated data and return it
        data['user'] = user
        return data

class UserDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Tbuser
        fields = ['cvid', 'ccname', 'ccemail', 'ccpassword', 'cvusertype']
        
class UserSerializer(serializers.ModelSerializer):
    cvusertype = serializers.IntegerField()

    class Meta:
        model = Tbuser
        fields = ['cvid', 'ccname', 'ccemail', 'ccpassword', 'cvusertype']

    def create(self, validated_data):
       
        user_type_id = validated_data.pop('cvusertype')
        user_type = Tbusertype.objects.get(cvid=user_type_id)

        # Hash the password before saving
        validated_data['ccpassword'] = make_password(validated_data['ccpassword'])

        # Create the user instance
        user = Tbuser.objects.create(cvusertype=user_type, **validated_data)
        return user

    def update(self, instance, validated_data):
       
        user_type_id = validated_data.pop('cvusertype', None)
        if user_type_id:
            instance.cvusertype = Tbusertype.objects.get(cvid=user_type_id)

        # Update fields
        instance.ccname = validated_data.get('ccname', instance.ccname)
        instance.ccemail = validated_data.get('ccemail', instance.ccemail)
        
        # If password is provided, hash it
        if 'ccpassword' in validated_data:
            instance.ccpassword = make_password(validated_data['ccpassword'])

        instance.save()
        return instance
