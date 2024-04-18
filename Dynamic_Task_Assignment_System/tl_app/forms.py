from django import forms
from tl_app.models import * 
from accounts.models import *

# class TaskForm(forms.ModelForm):
#     class Meta:
#         model = Task
#         field = ['employee','project','name','description','deadline']
#         exclude = ['status']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['employee'].required = True
#         self.fields['project'].required = True
#         self.fields['name'].required = True
#         self.fields['description'].required = True
#         self.fields['deadline'].required = True

#         # data_tl = UserProfile.objects.get(user=self.request.user)
#         # tllocation = data_tl.location
#         # self.fields['employee'].queryset = User.objects.filter(role=3,userprofile__location=tllocation)
#         self.fields['employee'].queryset = User.objects.filter(role=3)

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['employee', 'project', 'name', 'description', 'deadline','priority']

        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user_location = kwargs.pop('user_location', None)
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        for field in ['employee', 'project', 'name', 'description', 'deadline','priority']:
            self.fields[field].required = True

        if user_location:
            self.fields['employee'].queryset = User.objects.filter(role=3,userprofile__location=user_location)

        if user:
            self.fields['project'].queryset = Project.objects.filter(teamlead=user)
