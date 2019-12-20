from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _


class AuthForm(forms.Form):
    username = forms.CharField(label=_(u'Username'), widget=forms.TextInput(attrs={'placeholder': _(u'Username')}))
    password = forms.CharField(label=_(u'Password'), widget=forms.PasswordInput(attrs={'placeholder': _(u'Password')}))
    fields = ['username', 'password']
    
    def get_user(self):
        user = authenticate(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'])
        return user
