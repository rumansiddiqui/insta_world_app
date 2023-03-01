from django.contrib import admin
from django.urls import path

from account.views import UserViewCR

urlpatterns = [
    path('', UserViewCR.as_view()),

]
