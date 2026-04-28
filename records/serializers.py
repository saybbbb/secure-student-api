from rest_framework import serializers
from .models import StudentRecord

class StudentRecordSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = StudentRecord
        fields = '__all__'
