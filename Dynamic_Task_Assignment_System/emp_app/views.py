from django.shortcuts import render,get_object_or_404,redirect
from emp_app.forms import *
from tl_app.models import *
from django.contrib.auth.decorators import login_required
# Create your views here.
def employee_dashboard(request):
    return render(request,'emptemp/index.html')

@login_required(login_url='sign-in')
def task_view_employee(request):
    data = Task.objects.filter(employee=request.user)
    context = {'data':data}
    return render(request,'emptemp/tasks.html',context)

@login_required(login_url='sign-in')
def update_task_status(request, pk):
    if request.method == 'POST':
        form = TaskStatusForm(request.POST)
        if form.is_valid():
            data = Task.objects.get(id=pk)
            data.status=form.cleaned_data['status']
            data.save()
            return redirect('task-view-employee')
    else:
        form = TaskStatusForm()
    return render(request,'emptemp/update_tasks.html', {'form': form})

@login_required(login_url='sign-in')
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('view-message')
    else:
        form = MessageForm()
    return render(request, 'emptemp/send_message.html', {'form': form})

@login_required(login_url='sign-in')
def view_message(request):
    data = Message.objects.filter(sender=request.user)
    return render(request,'emptemp/view_message.html',{'data':data})

@login_required(login_url='sign-in')
def employee_views(request):
    data = User.objects.filter(role=3)
    emp = UserProfile.objects.filter(user__in=data)
    return render(request,'emptemp/emp_view.html',{'emp':emp})

@login_required(login_url='sign-in')
def teamlead_views(request):
    data = User.objects.filter(role=2)
    tl = UserProfile.objects.filter(user__in=data)
    return render(request,'emptemp/tl_view.html',{'tl':tl})