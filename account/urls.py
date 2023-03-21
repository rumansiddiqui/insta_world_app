from django.urls import path
from rest_framework import routers
from .views import SignUpAPI, ProfileAPI, PostAPI, CommentAPI
from rest_framework_simplejwt.views import (
    TokenObtainPairView as login,
    TokenRefreshView as refreshlogin,
)

router = routers.SimpleRouter()
router.register('signupapi', SignUpAPI, 'signupapi')
router.register('profile', ProfileAPI, 'profile')
router.register('post', PostAPI, 'post')
router.register('postcomment', CommentAPI, 'postcomment')

urlpatterns = [
                  path('login/', login.as_view(), name='login'),
                  path('refreshlogin/', refreshlogin.as_view(), name='refreshlogin'),
              ] + router.urls
