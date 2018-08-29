from django.contrib import admin
from django.urls import path,include
# from django.conf.urls import include,url

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r"", include("home.urls", namespace="home")),
]
