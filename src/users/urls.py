from django.urls import path
from .views import register_view, terms_view, login_view, account_view, host_register_view, logout_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("register/", register_view, name="register"),
    path("terms/", terms_view, name="terms"),
    path("login/", login_view, name="login"),

    path("reset_password/",
         auth_views.PasswordResetView.as_view(template_name="users/reset_password.html"),
         name="reset_password"),
    path("reset_password_sent/",
         auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_sent.html"),
         name="password_reset_done"),
    path("reset/<uidb64>/<token>/",
         auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"),
         name="password_reset_confirm"),
    path("reset_password_complete/",
         auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
         name="password_reset_complete"),
    path("account/",
         account_view,
         name="account"),
    path('logout/',
         logout_view,
         name='logout'),
    path("host_register/",
         host_register_view,
         name="host_register"),
]
