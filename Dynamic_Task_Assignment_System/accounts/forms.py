from django import forms
from accounts.models import *

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email','password']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username is already in use')
        return username
    
    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


LOCATIONS = (
    ('Kochi', 'Kochi'),
    ('Trivandrum', 'Trivandrum'),
    ('Calicut', 'Calicut'),
)

class TeamleadRegistrationForm(forms.ModelForm):
    name = forms.CharField(required=True)
    photo = forms.ImageField(required=True)
    location = forms.ChoiceField(choices=LOCATIONS,required=True)
    class Meta:
        model = UserProfile
        fields = ['name', 'mobile_number','photo','location']

class EmployeeRegistrationForm(forms.ModelForm):
    name = forms.CharField(required=True)
    photo = forms.ImageField(required=True)
    location = forms.ChoiceField(choices=LOCATIONS,required=True)
    position = forms.CharField(required=True)
    class Meta:
        model = UserProfile
        fields = ['name', 'mobile_number','photo','location','position']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['teamlead','name', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teamlead'].queryset = User.objects.filter(role=2)