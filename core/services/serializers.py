from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = []
        # Uncomment the following line to display some of the fields for django.contrib.auth.models.User
        # fields = ['username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = []
        # Uncomment the following line to display some of the fields for django.contrib.auth.models.Group
        # fields = ['name', 'permissions']