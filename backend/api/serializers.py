from rest_framework import serializers
from django.contrib.auth.models import User
from .models import PentestVulnerability, PentestExploit, PentestPatch

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'date_joined']

class PentestVulnerabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PentestVulnerability
        fields = ['id', 'name', 'description', 'location', 'cve']

class PentestExploitSerializer(serializers.ModelSerializer):
    class Meta:
        model = PentestExploit
        fields = ['id', 'description']

class PentestPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = PentestPatch
        fields = ['id', 'description']