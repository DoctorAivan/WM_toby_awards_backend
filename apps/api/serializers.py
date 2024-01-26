from rest_framework import serializers
from apps.api.models import Vote


class AccountSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    email = serializers.EmailField()
    token = serializers.CharField()


class RegistrationSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField()
    email = serializers.EmailField()
    token = serializers.CharField()


class VoteSerializer(serializers.Serializer):
    form = serializers.IntegerField()
    votes = serializers.CharField()
    token = serializers.CharField()
