from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ModelChoiceField(queryset=Group.objects.all())

    class Meta():
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'role']

        # excludes=[]

        label = {
            'password': 'Password'
        }

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            initial = kwargs.setdefault('initial', {})
            if kwargs['instance'].groups.all():
                initial['role'] = kwargs['instance'].groups.all()[0]
            else:
                initial['role'] = None
        forms.ModelForm.__init__(self, *args, **kwargs)


    def save(self):
        password = self.cleaned_data.pop('password')
        role = self.cleaned_data.pop('role')
        u = super().save()
        u.groups.set([role])
        u.set_password(password)
        u.save()
        return u