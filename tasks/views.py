from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from .models import Task
from .serializers import TaskSerializer
from .permissions import IsOwnerOrAdmin


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['completed']

    def get_queryset(self):
        user = self.request.user

        # for detail actions we need all tasks so permission check works correctly
        # otherwise non-owners get 404 instead of 403 which is wrong
        if self.action in ('retrieve', 'update', 'partial_update', 'destroy'):
            return Task.objects.all()

        # for listing, admin sees everything, normal users see their own tasks
        if user.is_authenticated:
            if user.role == 'admin':
                return Task.objects.all()
            return Task.objects.filter(user=user)

        # unauthenticated can only read, so show all
        return Task.objects.all()

    def perform_create(self, serializer):
        # assign task to the logged in user
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # double checking auth here just to be safe
        if not request.user.is_authenticated:
            return Response(
                {'error': 'you need to login first'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        task_obj = self.get_object()
        self.check_object_permissions(request, task_obj)
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(task_obj, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        task_obj = self.get_object()
        self.check_object_permissions(request, task_obj)
        task_obj.delete()
        return Response({'message': 'task deleted succesfully'}, status=status.HTTP_204_NO_CONTENT)
