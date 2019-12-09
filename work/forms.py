from django import forms
from .models import WorkTime, WorkPlace

class CreateWorkTime(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['workplace'].queryset = forms.ModelChoiceField(queryset=WorkPlace.objects.filter(worker_id=kwargs['id']))
    class Meta:
        model = WorkTime
        fields = ('workplace', 'date_start', 'date_end')
