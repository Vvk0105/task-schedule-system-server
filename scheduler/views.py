from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task, TaskExecutionHistory
from .utils import get_next_run_time
from croniter import croniter
from datetime import datetime

# Create your views here.

@api_view(['POST'])
def create_task(request):
    name = request.data.get('name')
    cron = request.data.get('cron_expression')
    depends = request.data.get('depends_on')

    if not cron:
        return Response({"error": "cron_expression is required"}, status=400)

    if depends and str(depends) == str(name):
        return Response({"error": "Task cannot depend on itself"}, status=400)

    # create task
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

@api_view(['POST'])
def pause_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.is_paused = True
    task.save()
    return Response({"message": "Task paused"})


@api_view(['POST'])
def resume_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.is_paused = False
    task.save()
    return Response({"message": "Task resumed"})

@api_view(['POST'])
def run_now(request, task_id):
    task = Task.objects.get(id=task_id)

    TaskExecutionHistory.objects.create(
        task=task,
        status="manual",
        log="Task executed manually"
    )

    task.next_run_at = get_next_run_time(task.cron_expression)
    task.save()

    return Response({"message": "Task executed manually"})

@api_view(['POST'])
def cron_preview(request):
    cron = request.data.get("cron_expression")

    if not cron:
        return Response({"error": "cron_expression required"}, status=400)

    now = datetime.now()
    itr = croniter(cron, now)

    next_times = []
    for _ in range(5):
        next_times.append(itr.get_next(datetime).strftime("%Y-%m-%d %H:%M:%S"))

    return Response({"next_runs": next_times})

@api_view(['GET'])
def execution_history(request):
    task_id = request.GET.get('task_id')
    status = request.GET.get('status')

    logs = TaskExecutionHistory.objects.all()

    if task_id:
        logs = logs.filter(task_id=task_id)

    if status:
        logs = logs.filter(status=status)

    data = [{
        "task": log.task.name,
        "status": log.status,
        "log": log.log,
        "start_time": log.start_time,
        "end_time": log.end_time
    } for log in logs]

    return Response(data)

@api_view(['GET'])
def dashboard_stats(request):

    total_tasks = Task.objects.count()
    total_executions = TaskExecutionHistory.objects.count()
    success_count = TaskExecutionHistory.objects.filter(status="success").count()
    failure_count = TaskExecutionHistory.objects.filter(status="failed").count()

    success_rate = 0
    if total_executions > 0:
        success_rate = (success_count / total_executions) * 100

    upcoming = Task.objects.filter(is_active=True).order_by('next_run_at')[:5]

    upcoming_list = [{
        "task": t.name,
        "next_run_at": t.next_run_at
    } for t in upcoming]

    return Response({
        "total_tasks": total_tasks,
        "total_executions": total_executions,
        "success_count": success_count,
        "failure_count": failure_count,
        "success_rate": success_rate,
        "upcoming": upcoming_list
    })
