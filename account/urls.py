from django.urls import path

from account.views import UserModelApi, UpdateDeleteApi

urlpatterns = [
    path('', UserModelApi.as_view()),
    path('user/<int:pk>/', UpdateDeleteApi.as_view()),

]
