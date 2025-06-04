from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import QuesModel, Category, UserProfile

# Your form classes will go here 

class addQuestionform(forms.ModelForm):
    class Meta:
        model = QuesModel
        fields = ['question', 'op1', 'op2', 'op3', 'op4', 'ans', 'category', 'points', 'time_limit']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'op1': forms.TextInput(attrs={'class': 'form-control'}),
            'op2': forms.TextInput(attrs={'class': 'form-control'}),
            'op3': forms.TextInput(attrs={'class': 'form-control'}),
            'op4': forms.TextInput(attrs={'class': 'form-control'}),
            'ans': forms.TextInput(attrs={'class': 'form-control'}),
            'time_limit': forms.NumberInput(attrs={'class': 'form-control'}),
            'points': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class createuserform(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create UserProfile for the new user
            UserProfile.objects.get_or_create(user=user)
        return user

class CustomPasswordResetForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )

class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter new password'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        })

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        } 