from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from projects.models import Project
from projects.serializers.projects_serializers import (
    ProjectSerializer, ProjectDetailSerializer, ProjectCreateSerializer
)
from accounts.models import User
from permissions import (
    IsAdminUser, IsProjectManager, IsAdminOrProjectManager, IsAdminOrProjectManagerOrMember
)
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        permissions = [IsAuthenticated()]

        if self.action == 'create':
            permissions.append(IsAdminUser())
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions.append(IsAdminOrProjectManager())
        elif self.action in ['retrieve', 'list']:
            permissions.append(IsAdminOrProjectManagerOrMember())
        elif self.action in ['add_member', 'remove_member']:
            permissions.append(IsAdminOrProjectManager())

        return permissions

    def get_serializer_class(self):
        if self.action == 'create':
            return ProjectCreateSerializer
        elif self.action in ['retrieve', 'list']:
            return ProjectDetailSerializer
        return ProjectSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Project.objects.all()

        return Project.objects.filter(
            Q(manager=user) |
            Q(members=user)
        ).distinct()

    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        project = self.get_object()
        user_id = request.data.get('user_id')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'المستخدم غير موجود.'}, status=status.HTTP_400_BAD_REQUEST)

        project.members.add(user)
        return Response({'message': 'تمت إضافة العضو بنجاح.'})

    @action(detail=True, methods=['post'])
    def remove_member(self, request, pk=None):
        project = self.get_object()
        user_id = request.data.get('user_id')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'المستخدم غير موجود.'}, status=status.HTTP_400_BAD_REQUEST)

        project.members.remove(user)
        return Response({'message': 'تمت إزالة العضو بنجاح.'})
