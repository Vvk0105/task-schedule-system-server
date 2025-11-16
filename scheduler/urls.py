from django.urls import path
from . import views

urlpatterns = [
    path('create-task/', views.create_task),
    path('tasks/', views.list_tasks),
    path('task/<int:task_id>/edit/', views.edit_task),
    path('task/<int:task_id>/delete/', views.delete_task),

    path('task/<int:task_id>/pause/', views.pause_task),
    path('task/<int:task_id>/resume/', views.resume_task),

    path('task/<int:task_id>/run-now/', views.run_now),

    path('cron-preview/', views.cron_preview),
    path('execution-history/', views.execution_history),
    path('dashboard-stats/', views.dashboard_stats),


]
