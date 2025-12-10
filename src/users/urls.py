from django.urls import path
from .views import register_view, terms_view, login_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('terms/', terms_view, name='terms'),
    path('login/', login_view, name='login'),
]
