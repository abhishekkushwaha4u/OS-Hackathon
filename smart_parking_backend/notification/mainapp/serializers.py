from rest_framework import serializers

from .models import UserNotification, BulkMessageIssuer


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserNotification
        fields = ['mobile', 'password']


class BulkMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = BulkMessageIssuer
        fields = "__all__"
