from django import forms
from django.contrib.auth.forms import UserCreationForm

from core.models import Worker


class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['first_name', 'last_name', 'date_hired', 'salary', 'position']


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'password1', 'password2', 'first_name']
