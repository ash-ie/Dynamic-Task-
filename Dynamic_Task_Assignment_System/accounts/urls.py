from django.urls import path
from accounts import views

urlpatterns = [
    path('',views.index,name='index'),
    path('admin-dashboard/',views.admin_dashboard,name='admin-dashboard'),
    path('tl-signup/',views.tl_signup,name='tl-signup'),
    path('tl-view/',views.tl_view,name='tl-view'),
    path('emp-signup/',views.emp_signup,name='emp-signup'),
    path('emp-view/',views.emp_view,name='emp-view'),
    path('project-create/',views.project_create,name='project-create'),
    path('project-view/',views.project_view,name='project-view'),
    path('sign-in/',views.login_view,name='sign-in'),
    path('sign-out/',views.sign_out,name='sign-out'),
    path('task-list/', views.view_tasks, name='task-list'),
    path('report-list-admin/', views.project_report_admin, name='report-list-admin'),
]