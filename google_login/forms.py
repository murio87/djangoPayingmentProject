from django import forms
from django.contrib.auth.forms import UserCreationForm
from google_login.models import AccountPeople
from django.contrib.auth import authenticate


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=30, help_text='Required, add a valid email address')

    class Meta:
        model = AccountPeople
        fields = ('email', 'first_name', 'last_name', 'username', 'password1', 'password2')


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = AccountPeople
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid Password or Email')


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = AccountPeople
        fields = ('email', 'username', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            try:
                account = AccountPeople.objects.exclude(pk=self.instance.pk).get(email=email)
                raise forms.ValidationError('Email "%s" is already in use.' % email)
            except AccountPeople.DoesNotExist:
                return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            try:
                account = AccountPeople.objects.exclude(pk=self.instance.pk).get(username=username)
                raise forms.ValidationError('Username "%s" is already in use.' % username)
            except AccountPeople.DoesNotExist:
                return username
