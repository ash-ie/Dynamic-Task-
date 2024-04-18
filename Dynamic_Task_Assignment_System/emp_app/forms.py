from django import forms
from tl_app.models import *
from accounts.models import *
from emp_app.models import *

class TaskStatusForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recipient'].queryset = User.objects.filter(role=2)