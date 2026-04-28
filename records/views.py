from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import StudentRecord
from .serializers import StudentRecordSerializer
from .permissions import IsAdminUser, IsAdminOrFaculty, IsOwnerOrAdminOrFaculty


class StudentRecordViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Student Records.
    
    Access Control:
    - CREATE / DELETE  → Admin only
    - UPDATE           → Admin or Faculty
    - LIST / RETRIEVE  → Any authenticated user (students see only their own)
    """
    queryset = StudentRecord.objects.all()
    serializer_class = StudentRecordSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            permission_classes = [IsAdminUser]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAdminOrFaculty]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsOwnerOrAdminOrFaculty]
        else:  # list
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user

        # Admin and Faculty see all records
        if user.groups.filter(name__in=['Admin', 'Faculty']).exists():
            return StudentRecord.objects.all()

        # Students see only their own records
        return StudentRecord.objects.filter(owner=user)

    def perform_create(self, serializer):
        """Automatically set the owner to the requesting user (or allow admin to specify)."""
        serializer.save(owner=self.request.user)
