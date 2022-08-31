from .models import Profile
from account.models import Account
from django import forms
from django.contrib.auth import models
from django.db.models import fields

# creates the profile update form
class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('department','batch','reg_num','mobile_num','designation')

    
# creates the account update form
class AccoutUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('email', 'first_name', 'last_name','image')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('There is already an account with Email "%s" ' % account)

    def clean_first_name(self):
        username = self.cleaned_data['first_name']
        if len(username)==0:
            raise forms.ValidationError('Sorry! First name can not be empty')
        return username

    def clean_image(self):
        image = self.cleaned_data['image']
        return image

    def save(self, commit=True):
        account = self.instance
        account.email = self.cleaned_data['email']
        account.first_name = self.cleaned_data['first_name']
        account.last_name = self.cleaned_data['last_name']

        if self.cleaned_data['image']:
            account.image = self.cleaned_data['image']
        if commit:
            account.save()
        return account