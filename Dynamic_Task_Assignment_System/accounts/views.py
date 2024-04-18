import logging

from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from tl_app.views import project_completion_report, project_progress_report
logger = logging.getLogger(__name__)
from accounts.forms import *
from tl_app.models import *

# Create your views here.
def index(request):
    return render(request,'index.html')

def admin_dashboard(request):
    return render(request,'admintemp/index.html')

def login_view(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None and user.is_active:
                login(request, user)
                if user.role == 1:
                    return redirect('admin-dashboard')
                elif user.role == 2:
                    return redirect('tl-dashboard')
                elif user.role == 3:
                    return redirect('emp-dashboard')
            else:
                messages.info(request, 'Invalid Credentials or User is not active')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
    return render(request, 'login.html')

def sign_out(request):
    logout(request)
    return redirect('/')

@login_required(login_url='sign-in')
def tl_signup(request):
    if request.method == 'POST':
        form = TeamleadRegistrationForm(request.POST,request.FILES)
        u_form = UserRegistrationForm(request.POST)
        if form.is_valid() and u_form.is_valid():
            user = u_form.save(commit=False)
            user.role = 2
            user.is_active = True
            user.save()
            customer = form.save(commit=False)
            customer.user = user
            customer.save()
            return redirect('tl-view') 
    else:
        form = TeamleadRegistrationForm()
        u_form = UserRegistrationForm()
    return render(request,'admintemp/tl_register.html',{'form':form,'u_form':u_form})

@login_required(login_url='sign-in')
def emp_signup(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST, request.FILES)
        u_form = UserRegistrationForm(request.POST)
        if form.is_valid() and u_form.is_valid():
            user = u_form.save(commit=False)
            user.role = 3
            user.is_active = True
            user.save()
            customer = form.save(commit=False)
            customer.user = user
            customer.save()
            return redirect('emp-view')
        else:
            logger.error('Form validation failed. Form errors: %s, %s', form.errors, u_form.errors)
    else:
        form = EmployeeRegistrationForm()
        u_form = UserRegistrationForm()
    return render(request, 'admintemp/emp_register.html', {'form': form, 'u_form': u_form})

@login_required(login_url='sign-in')
def tl_view(request):
    data = User.objects.filter(role=2)
    tl = UserProfile.objects.filter(user__in=data)
    return render(request, 'admintemp/tl_view.html', {'tl': tl})

@login_required(login_url='sign-in')
def emp_view(request):
    data = User.objects.filter(role=3)
    emp = UserProfile.objects.filter(user__in=data)
    return render(request, 'admintemp/emp_view.html', {'emp': emp})

@login_required(login_url='sign-in')
def view_tasks(request):
    data = Task.objects.all()
    context = {'data':data}
    return render(request,'admintemp/tasks.html',context)

@login_required(login_url='sign-in')
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project-view')
    else:
        form = ProjectForm()
    context = {
        'form': form
    }
    return render(request, "admintemp/project_create.html", context)

@login_required(login_url='sign-in')
def project_view(request):
    data = Project.objects.all()
    context = {'data':data}
    return render(request,'admintemp/projects.html',context)

@login_required(login_url='sign-in')
def project_report_admin(request):
    projects = Project.objects.all()
    data = []
    for project in projects:
        completion_rate = project_completion_report(project)
        progress_rate = project_progress_report(project)
        data.append({
            'project_name': project.name,
            'completion_rate': completion_rate,
            'progress_rate': progress_rate,
        })
    context = {'data': data}
    return render(request, 'admintemp/project_report.html', context)