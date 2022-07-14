from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from accounts.forms import SignupForm

# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = AuthenticationForm(request = request, data = request.POST)
        if form.is_valid():
            loggedInUser = loginUser(request, form)
            if loggedInUser is not None:
                return redirect('/')
        else:
            messages.add_message(request, messages.ERROR, 'Username/Password is incorrect!')

    return render(request, 'accounts/login.html')

def loginUser(request, form):
    username = form.cleaned_data.get('username')
    password = form.cleaned_data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)

        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)

    return user

@login_required
def logout_view(request):
    logout(request)

    return redirect('/')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    form = SignupForm()
    context = {'form': form}

    return render(request, 'accounts/signup.html', context)
