from django.urls import path

from account import views
from account.views import UserModelApi
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("user", views.UserModelApi)
router.register("signup", views.SignUpApi)
router.register("signin", views.SignInApi)
urlpatterns = [

]+router.urls

