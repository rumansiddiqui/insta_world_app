from account import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("signup", views.SignUpApi, basename="signup")
router.register("signin", views.SignInApi, basename="signin")
router.register("profile", views.ProfileApi, basename="profile")
router.register("post", views.PostApi, basename="post")
router.register("changepassword", views.ChangePasswordApi, basename="changepassword")
router.register("userfollowerspost", views.UserFollowersPostApi, basename="followerspost")
router.register("alluserpost", views.AllUserPostApi, basename="alluserpost")
router.register("userlikespost", views.UserPostLikeApi, basename="userlikespost")
router.register("savedpost", views.PostsSavedAPIView, basename="savedpost")
# router.register("Commentpost", views.CommentApi, basename="commentpost")
router.register("particularuserpost", views.PostListView, basename="particularuserpost")
router.register("particularuserpostlike", views.PostLikeView, basename="particularuserpostlike")
urlpatterns = [

]+router.urls

