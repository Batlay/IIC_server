from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import *


class TaskSerializer(ModelSerializer):
    created_on = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    author = serializers.CharField(source="author.username", read_only=True)
    pupil = serializers.CharField(source="pupil.fio", read_only=True)

    class Meta:
        model = Task
        fields = '__all__'


class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_superuser', 'groups', 'first_name', 'last_name')
