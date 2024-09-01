from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm


def register_user(request: HttpRequest):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        print('form ok')
        if form.is_valid():
            print('form is valid. ok')
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            print('user: ', user)
            login(request, user)
            messages.success(request, 'Account is created successfully!')
            return redirect('home')
    else:
        print('hello-3')
        form = RegisterUserForm()

    return render(request, 'authenticate/register_user.html', {
        'form': form
    })

def logout_user(request: HttpRequest):
    logout(request)
    messages.success(request, "You were logging out")
    return redirect('home')

def login_user(request: HttpRequest):

    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('home')
        else:
            # Return an 'invalid login' error message.
            messages.success(request, ('There was an error logged in. Try again later.'))
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html', {})


