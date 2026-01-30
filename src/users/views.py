from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import RegistrationForm, HostRegistrationForm, LoginForm


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            return redirect("users:main_page")
    else:
        form = RegistrationForm()

    return render(request, template_name="users/register.html", context={"form": form})

def terms_view(request):
    return render(request, template_name="users/terms.html")


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("users:main_page")
    else:
        form = LoginForm()

    return render(request, template_name="users/login.html", context={"form": form})

def mainpage_view(request):
    return render(request, template_name="users/main_page.html")


def host_register_view(request):
    if request.method == 'POST':
        form = HostRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('users:main_page')
    else:
        form = HostRegistrationForm()

    return render(request, 'users/host_register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('users:login')
