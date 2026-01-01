from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegistrationForm()

    return render(request, template_name="users/register.html", context={"form": form})


def terms_view(request):
    return render(request, template_name="users/terms.html")


def login_view(request):
    return render(request, template_name="users/login.html")

