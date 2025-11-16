from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task
from .utils import get_next_run_time

# Create your views here.

@api_view(['POST'])
def create_task(request):
    name = request.data.get('name')
    cron = request.data.get('cron_expression')
    depends = request.data.get('depends_on')

    task = Task.objects.create(
        name=name,
        cron_expression=cron,
        depends_on_id=depends if depends else None,
        next_run_at=get_next_run_time(cron)
    )

    return Response({"message": "Task created", "task_id": task.id})

@api_view(['GET'])
def list_tasks(request):
    tasks = Task.objects.all().values()
    return Response(list(tasks))

@api_view(['PUT'])
def edit_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.name = request.data.get('name', task.name)
    task.cron_expression = request.data.get('cron', task.cron_expression)
    task.next_run_at = get_next_run_time(task.cron_expression)
    task.save()
    return Response({"message": "Task updated"})

@api_view(['DELETE'])
def delete_task(request, task_id):
    Task.objects.get(id=task_id).delete()
    return Response({"message": "Task deleted"})