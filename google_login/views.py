from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from google_login.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm


def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            account = authenticate(email=email, password=password, first_name=first_name, last_name=last_name)
            login(request, account)
            print('Redirecting to login page')
            return redirect('login')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'google_login/register.html', context)


def login_view(request):
    context = {}
    user = request.user
    # if user.is_authenticated:
    #	return redirect('home')
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('home')
    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form
    return render(request, 'google_login/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    context = {}
    if request.method == 'POST':
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating profile. Please correct the errors below.')
    else:
        form = AccountUpdateForm(
            instance=request.user,
            initial={
                'email': request.user.email,
                'username': request.user.username,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
            }
        )

    context['profile_form'] = form
    return render(request, 'google_login/profile.html', context)
