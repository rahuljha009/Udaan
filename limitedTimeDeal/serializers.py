from rest_framework import serializers
from limitedTimeDeal import models


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password', 'isSeller')


class DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Deal
        fields = ('__all__')

