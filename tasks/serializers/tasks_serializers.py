from rest_framework import serializers
from tasks.models import  Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'project', 'title', 'description', 'assigned_to', 'is_completed', 'created_at']

    def validate(self, data):
        project = data.get('project')
        assigned_to = data.get('assigned_to')

        if assigned_to and assigned_to not in project.members.all():
            raise serializers.ValidationError("يمكنك فقط تكليف أعضاء ضمن المشروع.")
        return data
