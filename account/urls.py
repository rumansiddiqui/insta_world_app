from account import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

# router.register("user", views.UserModelApi, basename="user")
router.register("signup", views.SignUpApi, basename="signup")
router.register("signin", views.SignInApi, basename="signin")
router.register("profile", views.ProfileApi, basename="profile")
router.register("post", views.PostApi, basename="post")
urlpatterns = [

]+router.urls

