from django.conf.urls import url
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

app_name = "home"

urlpatterns = [
    path("", views.homepage, name="home"),
    path("signup/", views.signup, name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name= "home/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/login"), name="logout"),
    path("comment/<int:post_id>", views.comments, name="post-detail"),
    path("usr/<username>", views.profile, name="profile"),
    path("follow/<username>", views.createFollow, name="follow"),
    path("unfollow/<userid>",views.unFollow,name="unfollow"),
    path("updateprofile/<username>", views.update_profile,name="update-profile"),
    path("q/search", views.search, name="search"),
    path("createcomment", views.createComment, name="create-comment"),
    path("createlike", views.createLike, name="create-like"),
    path("unlike", views.unLike, name="unlike"),
    path("post/<int:post_id>", views.postDetails, name="post-detail"),
    path("createpost", views.createPost, name="create-post"),
    path("createreport",views.createReport, name="create-report"),
    path("deletepost", views.deletePost, name="post-delete"),
    path("updatepost/<int:id>", views.updatePost, name="post-update"),
    path("postinfo/<int:post>", views.postInfo, name="post-info"),
    path("userpic/<int:id>",views.profilePic,name="profilepic"),
    path("play/<vid>",views.playVideo),
    path("notifications/", views.notification),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)