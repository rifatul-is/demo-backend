from asyncio import all_tasks

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializer import TaskSerializer
from base.models import Task
# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tasks(request):
    user = request.user
    all_tasks = user.task_set.all()
    serializer = TaskSerializer(all_tasks, many=True)
    return Response(serializer.data)

