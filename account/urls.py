from django.urls import path

from account import views
from account.views import UserModelApi
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("user", views.UserModelApi)
router.register("signup", views.SignUpApi)
router.register("signin", views.SignInApi)
router.register("profile", views.ProfileApi)
router.register("post", views.PostApi)
urlpatterns = [

]+router.urls

