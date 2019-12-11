from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView

from django import forms
from .forms import *

from django.contrib import messages


class AccountsLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = ForBootStrapAuthenticationForm


class AccountsLogoutView(LogoutView):
    pass


def register(request):
    """회원가입하는 뷰"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            new_user = form.save(commit=False)
            """django 공식문서에 보면 비밀번호를 설정할때 User object로 바로 세이브 하지 말고
            set_password를 통해서 비밀번호를 설정해주고 세이브 하라고 나와있다."""
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()

            messages.info(request, '반갑습니다 ' + new_user.username + '님 로그인 해주세요.')
            return redirect('accounts:login')
        else:
            """비밀번호가 틀릴경우 Forms.ValidationError가 raise되어야 하지만
            어디서 raise가 되는지 모르겠다....
            그래서 그냥 field에 에러가 있을시 따로 메세지를 전송."""
            if form['password2'].errors:
                messages.warning(request, '비밀번호가 같지 않습니다.')

            elif form['username'].errors:
                messages.warning(request, '이미 있는 아이디입니다.')

    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})
# Create your views here.
