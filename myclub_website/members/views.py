from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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


