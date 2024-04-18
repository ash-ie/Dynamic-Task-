from django.urls import path
from tl_app import views

urlpatterns = [
    path('tl-dashboard/',views.tl_dashboard,name='tl-dashboard'),
    path('company-employee/',views.company_employee,name='company-employee'),
    path('project-tl/',views.project_view_tl,name='project-tl'),
    path('create-task/', views.create_task, name='create-task'),
    path('task-list/', views.view_tasks, name='task-list'),
    path('project-report/', views.project_report, name='project-report'),
    path('message-tl/', views.view_message_tl, name='message-tl'),
    path('reply-message/<int:id>/', views.reply_message, name='reply-message'),
]