from django import forms
from .models import WorkTime, WorkPlace


class CreateWorkTime(forms.ModelForm):
    # def __init__(self, w_id=None, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['workplace'].queryset = forms.ModelChoiceField(
    #                 queryset=WorkPlace.objects.filter(worker__id=1))

    class Meta:
        model = WorkTime
        fields = ('workplace', 'date_start', 'date_end')
