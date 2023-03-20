from account import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register("signup", views.SignUpApi, basename="signup")
router.register("signin", views.SignInApi, basename="signin")
router.register("profile", views.ProfileApi, basename="profile")
router.register("post", views.PostApi, basename="post")
router.register("changepassword", views.ChangePasswordApi, basename="changepassword")
router.register("userfollowerspost", views.UserFollowersPostApi, basename="followerspost")
router.register("alluserpost", views.AllUserPost, basename="alluserpost")
router.register("userlikespost", views.UserPostLikeApi, basename="userlikespost")
urlpatterns = [

]+router.urls

