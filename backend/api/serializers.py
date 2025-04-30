from rest_framework import serializers
from django.contrib.auth.models import User
from .models import PentestVulnerability, PentestExploit, PentestPatch, PentestProject, Code

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

# class PentestProjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PentestProject
#         fields = ['id', '']

# class CodeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Code
#         fields = []