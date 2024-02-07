from django.urls import path

from rest_framework_simplejwt.views import TokenBlacklistView

from .views import *


urlpatterns = [
    path("auth/logout/", TokenBlacklistView.as_view()),

    path("auth/email/", SendEmailView.as_view()),
    # path("auth/send-code/", SendEmailView.as_view()),
    path("auth/login/", LoginView.as_view()),
]