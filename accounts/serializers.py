from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=Profile.ROLE_CHOICES, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        role = validated_data.pop('role', 'employee')
        password = validated_data.pop('password')

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        user.profile.role = role
        user.profile.save()

        return user


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['role'] = instance.profile.role
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','first_name','last_name']

class EmployeeProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    class Meta:
        model = Profile
        fields = ['user','role']
