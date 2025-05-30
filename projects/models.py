from django.db import models
from django.conf import settings

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='managed_projects',
        on_delete=models.CASCADE
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='projects'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
