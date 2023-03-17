from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from account import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('login', views.UserLogIn, basename='login'),
router.register('register', views.UserRegister, basename='register'),
router.register('changepassword', views.UserChangePassword, basename='changepassword'),
router.register('deleteuser', views.DeleteUser, basename='deleteuser'),
router.register('post', views.UserPost, basename='post'),
router.register('profile', views.UserProfile, basename='profile'),
router.register('allpost', views.AllUserPost, basename='allpost')
router.register('followpost', views.UserFollowerPost, basename='followpost')


urlpatterns = [
    path('', include(router.urls))

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
