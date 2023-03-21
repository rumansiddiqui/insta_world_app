from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from post import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('allpost', views.AllUserPost, basename='allpost')
router.register('followpost', views.UserFollowerPost, basename='followpost')
router.register('post', views.UserPost, basename='post')


urlpatterns = [
    path('', include(router.urls))

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
