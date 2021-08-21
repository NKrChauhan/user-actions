from rest_framework import serializers
from .models import Task
from django.conf import settings
from django.contrib.auth import get_user_model


USER = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'initiated_by','assigned_by', 'assigned_to','completed']
        read_only_fields = ('id',)
