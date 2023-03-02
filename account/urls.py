from django.contrib import admin
from django.urls import path

from account import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('api', views.UserView)

urlpatterns = [
    # path('api', UserViewCR.as_view()),
    # path('api/<int:pk>/', UserViewRUD.as_view()),

]

urlpatterns += router.urls
