from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from allauth.account.forms import SignupForm



class ForBootStrapAuthenticationForm(AuthenticationForm):
    """form에 html언어?를 씌우기 위해서 원래 있던 폼 상속후 widgets만 달고 사용"""
    username = forms.CharField(label='아이디', widget=forms.TextInput(
        attrs={'class': 'form-control', 'style': 'width:300px; margin: 0 auto;'}
    ))
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'style': 'width:300px; margin: 0 auto;'}
    ))


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'style': 'width:300px; margin: 0 auto;'}))
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'style': 'width:300px; margin: 0 auto;'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'width:300px; margin: 0 auto;'}
            ),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'style': 'width:300px; margin: 0 auto;'}
            ),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'width:300px; margin: 0 auto;'}
            ),
            'first_name': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'width:300px; margin: 0 auto;'}
            )
        }

    def clean_password2(self):
        """비밀번호가 확인 됐는지 확인하는 함수"""
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('비밀번호 에러')
        return cd['password2']
