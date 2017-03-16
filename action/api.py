# from django.shortcuts import render

# Create your views here.
from action.models import UserData
from rest_framework import serializers
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView, ListCreateAPIView
)


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ('id', 'name', 'text', 'user',)


class UserDataDetail(RetrieveUpdateDestroyAPIView):
    """Return a specific user data, update it, or delete it."""
    serializer_class = UserDataSerializer
    queryset = UserData.objects.all()

    lookup_field = 'pk'


class UserDataList(ListCreateAPIView):
    """Return a list of user data or create new ones."""
    serializer_class = UserDataSerializer
    queryset = UserData.objects.all()
