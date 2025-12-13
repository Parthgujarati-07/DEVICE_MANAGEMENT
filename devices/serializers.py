from rest_framework import serializers
from .models import Device
from django.contrib.auth.models import User


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class DeviceSerializer(serializers.ModelSerializer):
    issued_to_name = serializers.SerializerMethodField()

    issued_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Device
        fields = [
            'id',
            'name',
            'device_types',
            'issued_to',
            'issued_to_name',
            'issued_date'
        ]

    def get_issued_to_name(self, obj):
        if obj.issued_to:
            return obj.issued_to.username
        return None
