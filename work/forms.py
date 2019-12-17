from django import forms
from .models import WorkTime, WorkPlace


class CreateWorkTime(forms.ModelForm):
    class Meta:
        model = WorkTime
        fields = ('date_start', 'date_end')

class ChangeStatusForm(forms.ModelForm):
    class Meta:
        model = WorkPlace
        fields = []
