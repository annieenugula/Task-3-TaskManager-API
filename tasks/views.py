from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Task, Category
from .serializers import (
    TaskSerializer,
    TaskListSerializer,
    CategorySerializer
)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    filterset_fields = ['status', 'priority', 'category']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'priority']

    def get_queryset(self):
        return Task.objects.filter(
            owner=self.request.user
        ).select_related('category')

    def get_serializer_class(self):
        if self.action == 'list':
            return TaskListSerializer
        return TaskSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], url_path='complete')
    def mark_complete(self, request, pk=None):
        task = self.get_object()
        task.status = 'completed'
        task.save()

        return Response(
            {'status': 'Task marked as completed'},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'], url_path='stats')
    def statistics(self, request):
        tasks = self.get_queryset()

        stats = {
            'total': tasks.count(),
            'pending': tasks.filter(status='pending').count(),
            'in_progress': tasks.filter(status='in_progress').count(),
            'completed': tasks.filter(status='completed').count(),
            'overdue': sum(1 for t in tasks if t.is_overdue),
        }

        return Response(stats)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)