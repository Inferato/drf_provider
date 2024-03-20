from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Transaction, Document


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount',]


class RegistrationForm(UserCreationForm):
    bio = forms.CharField(max_length=500, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'bio']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio']

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file']
