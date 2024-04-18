from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from accounts.models import *
from tl_app.forms import *
from emp_app.models import *
# Create your views here.
def tl_dashboard(request):
    return render(request,'tltemp/index.html')

@login_required(login_url='sign-in')
def company_employee(request):
    u = request.user
    data_tl = UserProfile.objects.get(user=u)
    tllocation = data_tl.location
    data = User.objects.filter(role=3,userprofile__location=tllocation)
    emp = UserProfile.objects.filter(user__in=data)
    return render(request,'tltemp/emp_view.html',{'emp':emp})

@login_required(login_url='sign-in')
def project_view_tl(request):
    data = Project.objects.filter(teamlead=request.user)
    context = {'data':data}
    return render(request,'tltemp/projects.html',context)

@login_required(login_url='sign-in')
def create_task(request):
    user_profile = UserProfile.objects.get(user=request.user)
    user_location = user_profile.location
    if request.method == 'POST':
        form = TaskForm(request.POST, user_location=user_location,user=request.user)
        if form.is_valid():
            taskobj=form.save(commit=False)
            taskobj.teamlead = request.user
            taskobj.save()
            return redirect('task-list')
    else:
        form = TaskForm(user_location=user_location,user=request.user)
    context = {'form': form}
    return render(request, 'tltemp/task_add.html', context)

@login_required(login_url='sign-in')
def view_tasks(request):
    u = request.user
    pro = Project.objects.filter(teamlead=request.user)
    data = Task.objects.filter(project__in=pro)
    context = {'data':data}
    return render(request,'tltemp/tasks.html',context)


def project_progress_report(project):
    total_tasks = project.tasks.count()
    in_progress_tasks = project.tasks.filter(status='IN_PROGRESS').count()
    progress_rate = (in_progress_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    return progress_rate


def project_completion_report(project):
    total_tasks = project.tasks.count()
    done_tasks = project.tasks.filter(status='DONE').count()
    completion_rate = (done_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    return completion_rate

@login_required(login_url='sign-in')
def project_report(request):
    projects = Project.objects.filter(teamlead=request.user)
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
    return render(request, 'tltemp/project_report.html', context)

@login_required(login_url='sign-in')
def view_message_tl(request):
    data = Message.objects.filter(recipient=request.user)
    return render(request,'tltemp/view_message.html',{'data':data})

@login_required(login_url='sign-in')
def reply_message(request, id):
    f = Message.objects.get(id=id)
    if request.method == 'POST':
        r = request.POST.get('reply')
        f.reply = r
        f.save()
        return redirect('message-tl')
    return render(request, 'tltemp/reply_message.html', {'f': f})