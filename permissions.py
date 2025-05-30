from rest_framework import permissions

# 📌 عامة: أدمن
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


# 📌 Project Permissions
class IsProjectManager(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.manager == request.user


class IsAdminOrProjectManager(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.role == 'admin' or obj.manager == request.user
        )


class IsAdminOrProjectManagerOrMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.role == 'admin' or
            obj.manager == request.user or
            request.user in obj.members.all()
        )
    
    
# 📌 Task Permissions
class IsTaskAssignee(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.assigned_to == request.user


class IsProjectManagerOfTask(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.project.manager == request.user


class IsAdminOrProjectManagerOrTaskAssignee(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_authenticated and (
            user.is_superuser or
            obj.project.manager == user or
            obj.assigned_to == user
        )
