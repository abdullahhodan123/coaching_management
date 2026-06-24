from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm
)

from .models import User, Student, ClassRoom


class StudentRegistrationForm(UserCreationForm):

    full_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Mohammad Rahman'})
    )

    school_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Dhaka Government High School'})
    )

    classroom = forms.ModelChoiceField(
        queryset=ClassRoom.objects.all()
    )

    guardian_phone_1 = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '01XXXXXXXXX'})
    )

    guardian_phone_2 = forms.CharField(
        max_length=20,
        required=False,          # ← False করা ভালো, model এও blank=True আছে
        widget=forms.TextInput(attrs={'placeholder': '01XXXXXXXXX (optional)'})
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'your_username'}),
            'email':    forms.EmailInput(attrs={'placeholder': 'email@example.com'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # password1 ও password2 Meta.widgets এ কাজ করে না,
        # তাই __init__ এ আলাদা করে set করতে হয়
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'placeholder': 'Minimum 8 characters'}
        )
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'placeholder': 'Repeat password'}
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'

        if commit:
            user.save()
            Student.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                school_name=self.cleaned_data['school_name'],
                classroom=self.cleaned_data['classroom'],
                guardian_phone_1=self.cleaned_data['guardian_phone_1'],
                guardian_phone_2=self.cleaned_data['guardian_phone_2']
            )

        return user


class TeacherRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'teacher_username'}),
            'email':    forms.EmailInput(attrs={'placeholder': 'teacher@example.com'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'placeholder': 'Minimum 8 characters'}
        )
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'placeholder': 'Repeat password'}
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'teacher'

        if commit:
            user.save()

        return user


class UserLoginForm(AuthenticationForm):

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'your_username'})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'})
    )