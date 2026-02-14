from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from .forms import RegistrationForm, HostRegistrationForm, LoginForm
from .models import Event
from django.contrib.auth.decorators import login_required


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            return redirect("account")
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
            return redirect("account")
    else:
        form = LoginForm()

    return render(request, template_name="users/login.html", context={"form": form})

def account_view(request):
    return render(request, template_name="users/account.html")


def host_register_view(request):
    if request.method == "POST":
        form = HostRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("account")
    else:
        form = HostRegistrationForm()

    return render(request, "users/host_register.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")

def event_detail(request, pk):
    # Fetch the event by ID, or 404 if not found
    event = get_object_or_404(Event, pk=pk)
    spots_left = event.max_guests - event.guests.count()

    context = {
        "event": event,
        "spots_left": spots_left,
    }
    return render(request, "users/event_detail.html", context)

@login_required
def book_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.user.is_host:
        return redirect('event_detail', pk=pk)

    if request.user not in event.guests.all() and event.guests.count() < event.max_guests:
        event.guests.add(request.user)

    return redirect("event_detail", pk=pk)


@login_required
def my_events(request):
    events = request.user.attended_events.all()

    return render(request, "users/my_events.html", {"events": events})
