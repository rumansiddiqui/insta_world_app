from django.urls import path, include

from account import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('login', views.UserLogIn, basename='login'),
router.register('register', views.UserRegister, basename='register'),
router.register('changepassword', views.UserChangePassword, basename='changepassword'),

urlpatterns = [
    path('', include(router.urls))

]


