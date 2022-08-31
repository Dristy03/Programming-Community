from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from account.models import Account, role_options

# Form for registering users
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=30, required=True)
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)

    role = forms.ChoiceField(choices=role_options, widget=forms.RadioSelect())

    class Meta:
        model = Account
        fields = ('email', 'first_name', 'last_name', 'role')

# Form used for authentication 
class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")

