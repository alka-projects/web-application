from django import forms
from web_app.models import student
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class studentform(forms.ModelForm):
    class Meta:
        model = student
        fields = '__all__'

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user