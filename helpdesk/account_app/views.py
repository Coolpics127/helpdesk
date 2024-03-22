from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import LoginForm

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return redirect('index')
            else:
                 messages.error(request, 'Неверный логин или пароль! Убедитесь в правильности вводимых данных')
                 #return render(request, 'account_app/login_page.html', {'form':form})
        else:
            return render(request, 'account_app/login_page.html')
    else:
            form = LoginForm()
    return render(request,'account_app/login_page.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('/account/login')
