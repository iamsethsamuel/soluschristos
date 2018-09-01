from django.db import models
from django.contrib.auth.models import User, AnonymousUser
from django.urls import reverse
from django.db.models.signals import post_save

class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField()
    dp = models.FileField(upload_to="profiles")
    phone = models.CharField(max_length=13, default=None)
    country = models.CharField(max_length=50,default=None)
    stateRegion = models.CharField(max_length=50, default=None)
    sex = models.CharField(max_length=6)
    def __str__(self):
        return "{}".format(self.user)

class Posts(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    content = models.TextField(max_length=10000, default="None")
    pic = models.FileField(upload_to="uploads", default="None")
    pic1 = models.FileField(upload_to="uploads", default="None")
    pic2 = models.FileField(upload_to="uploads", default="None")
    pic3 = models.FileField(upload_to="uploads", default="None")
    pic4 = models.FileField(upload_to="uploads", default="None")
    pic5 = models.FileField(upload_to="uploads", default="None")
    pic6 = models.FileField(upload_to="uploads", default="None")
    pic7 = models.FileField(upload_to="uploads", default="None")
    pic8 = models.FileField(upload_to="uploads", default="None")
    pic9 = models.FileField(upload_to="uploads", default="None")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return " Content: %s" % (self.content)

    def get_absolute_url(self):
        return reverse("home:index")


class Subscription(models.Model):
    subscribe = models.ForeignKey(User, on_delete=models.CASCADE)
    subscriber = models.CharField(max_length=200, default="None")
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return "Subcribe: {} {}".format(self.subscribe,self.subscriber)

    def get_absolute_url(self):
        return reverse("home:profile")


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Post: %s" % self.post

    def get_absolute_url(self):
        return reverse("home:home")


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    comment = models.CharField(max_length=10000)
    date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("home:create-comment")

    def __str__(self):
        return "comment: {}".format(self.comment)

class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    notified_user = models.CharField(max_length=50, default="None")
    item = models.CharField(max_length=20)
    post = models.TextField(default="None")
    comment = models.TextField(default="None")
    like = models.TextField(default="None")
    seen = models.BooleanField(default=False)
    def get_absolute_url(self):
        return reverse("home:notifications")
    def __str__(self):
        return "item: {}, user: {}".format(self.item,self.user)

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    comment =models.TextField(default="None")

    def get_absolute_url(self):
        return reverse("home:home")
    def __str__(self):
        return "{} {}".format(self.post, self.user)
