from django.urls import path
from . import views

urlpatterns = [
    path('create-task/', views.create_task),
    path('list-task/', views.list_tasks),
    path('edit-task/<int:task_id>/', views.edit_task),
    path('delete-task/<int:task_id>/', views.delete_task),

    path('task/<int:task_id>/pause/', views.pause_task),
    path('task/<int:task_id>/resume/', views.resume_task),

    path('task/<int:task_id>/run-now/', views.run_now),

    path('cron-preview/', views.cron_preview),

]
