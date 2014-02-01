from django import forms
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.forms import PasswordInput
from auth.models import User
from common.forms import ModelForm


class LoginForm(ModelForm):
    name = 'Login'
    urlname = 'login'
    valid_users = (0,)
    success_msg = 'Successful login'

    pwd = forms.CharField(label='Password', widget=PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'pwd')

    def clean(self):
        user = User.objects.filter(email=self.cleaned_data.get('email')).first()
        if user is None:
            raise ValidationError('The email does not exist in our database')
        if not check_password(self.cleaned_data['pwd'], user.pwd):
            raise ValidationError('The password is incorrect')
        return self.cleaned_data

    def _post_clean(self):
        pass  # ensure we don't clean the email to make sure it is unique