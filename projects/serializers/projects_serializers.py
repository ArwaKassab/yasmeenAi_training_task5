from rest_framework import serializers
from projects.models import Project
from accounts.models import User

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'manager', 'members', 'created_at']
        read_only_fields = ['created_at']

class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description', 'manager']

    def validate_manager(self, value):
        if not User.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("المدير المحدد غير موجود.")
        return value

class ProjectDetailSerializer(serializers.ModelSerializer):
    manager = serializers.StringRelatedField()
    members = serializers.StringRelatedField(many=True)
    tasks = serializers.StringRelatedField(many=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'manager', 'members', 'tasks', 'created_at']

