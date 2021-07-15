from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth import authenticate


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({"placeholder": "Email"})
        self.fields['password1'].widget.attrs.update({"placeholder": "Password"})
        self.fields['password2'].widget.attrs.update({"placeholder": "Confirm Password"})
        self.fields['auth_code'].widget.attrs.update({"placeholder": "Authentication Code"})
        self.fields['gpass'].widget.attrs.update({"placeholder": "Gmail Password"})

    class Meta:
        model = User
        fields = ('email', 'auth_code', 'gpass')   # Fields while signing up through the website


class LoginForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={"placeholder": "Email"}
        ),
    )
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={"placeholder": "Password"}
    ),)
    # auth_code = forms.CharField(
    #     required=True,
    #     max_length=10,
    #     widget=forms.TextInput(
    #         attrs={"placeholder": "Authentication Code", }
    #     ),
    # )
    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                # print('Not authenticated')
                raise forms.ValidationError("Invalid Details")
