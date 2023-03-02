from django.urls import path

from account import views
from account.views import UserModelApi
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("user_api", views.UserModelApi)
router.register("sign_api", views.SignUpApi)
router.register("signin_api", views.SignInApi)
urlpatterns = [

]+router.urls

