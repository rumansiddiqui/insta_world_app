from django.contrib import admin
from django.urls import path

from account.views import UserViewCR, UserViewRUD

urlpatterns = [
    path('api', UserViewCR.as_view()),
    path('api/<int:pk>/', UserViewRUD.as_view()),

]
