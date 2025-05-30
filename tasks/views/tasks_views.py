from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from tasks.models import Task
from tasks.serializers.tasks_serializers import TaskSerializer
from accounts.models import User
from projects.models import Project
from permissions import (
    IsAdminUser, IsProjectManager,
    IsAdminOrProjectManagerOrMember, IsTaskAssignee,
    IsProjectManagerOfTask, IsAdminOrProjectManagerOrTaskAssignee
)

from django_filters.rest_framework import DjangoFilterBackend
from tasks.filters import TaskFilter


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter
    def get_permissions(self):
        user = self.request.user

        if user.is_authenticated and user.role == 'admin':
            return [IsAuthenticated()]
        permissions = [IsAuthenticated()]

        if self.action == 'create':
            permissions.append(IsAdminUser())
        elif self.action in ['update', 'partial_update']:
            permissions.append(IsAdminOrProjectManagerOrTaskAssignee())
        elif self.action == 'destroy':
            permissions.append(IsAdminOrProjectManagerOrTaskAssignee())
        elif self.action == 'assign_member':
            permissions.append(IsProjectManagerOfTask())
        elif self.action in ['list', 'retrieve']:
            permissions.append(IsAdminOrProjectManagerOrMember())

        return permissions

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Task.objects.all()

        return Task.objects.filter(
            Q(project__manager=user) |
            Q(project__members=user)
        ).distinct()

    # عرض مهام مشروع معين
    @action(detail=False, methods=['get'], url_path='project-tasks/(?P<project_id>[^/.]+)')
    def project_tasks(self, request, project_id=None):
        user = request.user

        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({'error': 'المشروع غير موجود'}, status=status.HTTP_404_NOT_FOUND)

        # permission checked here
        if not IsAdminOrProjectManagerOrMember().has_object_permission(request, self, project):
            return Response({'error': 'غير مصرح لك بعرض مهام هذا المشروع'}, status=status.HTTP_403_FORBIDDEN)

        tasks = Task.objects.filter(project=project)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    # إضافة مهمة لمشروع
    @action(detail=False, methods=['post'], url_path='add-task-to-project')
    def add_task_to_project(self, request):
        user = request.user
        project_id = request.data.get('project_id')

        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({'error': 'المشروع غير موجود'}, status=status.HTTP_404_NOT_FOUND)

        if not (user.is_superuser or project.manager == user):
            return Response({'error': 'غير مصرح لك بإضافة مهمة لهذا المشروع'}, status=status.HTTP_403_FORBIDDEN)

        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # تكليف عضو بمهمة
    @action(detail=True, methods=['post'], url_path='assign-member')
    def assign_member(self, request, pk=None):
        task = self.get_object()
        user = request.user

        if not IsProjectManagerOfTask().has_object_permission(request, self, task):
            return Response({'error': 'غير مصرح لك بتكليف الأعضاء'}, status=status.HTTP_403_FORBIDDEN)

        member_id = request.data.get('member_id')

        try:
            member = User.objects.get(id=member_id)
        except User.DoesNotExist:
            return Response({'error': 'المستخدم غير موجود'}, status=status.HTTP_404_NOT_FOUND)

        project = task.project

        if member not in project.members.all():
            return Response({'error': 'هذا العضو غير موجود في المشروع'}, status=status.HTTP_400_BAD_REQUEST)

        task.assigned_to = member
        task.save()

        return Response({'message': f'تم تكليف {member.username} بالمهمة بنجاح'})

    @action(detail=False, methods=['get'], url_path='search')
    def search_tasks(self, request):
        query = request.query_params.get('q')
        if not query:
            return Response({'error': 'يرجى إدخال كلمة بحث.'}, status=400)
        
        tasks = Task.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)