from django.urls import path
from emp_app import views

urlpatterns = [
    path('emp-dashboard/',views.employee_dashboard,name='emp-dashboard'),
    path('task-view-employee/',views.task_view_employee,name='task-view-employee'),
    path('update-task-status/<int:pk>/',views.update_task_status,name='update-task-status'),
    path('send-message/',views.send_message,name='send-message'),
    path('view-message/',views.view_message,name='view-message'),
    path('employee-views/',views.employee_views,name='employee-views'),
    path('teamlead-views/',views.teamlead_views,name='teamlead-views'),
]