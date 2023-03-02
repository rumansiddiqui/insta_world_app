from django.urls import path
from rest_framework import routers

from . import views
from .views import SignUpAPI

router = routers.SimpleRouter()
router.register('signupapi', SignUpAPI, 'signupapi')

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
                  path('signup', views.sign_up, name='signup'),
                  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

              ] + router.urls
