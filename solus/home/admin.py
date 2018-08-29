from django.contrib import admin
from . models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
import subprocess
class UsersInline(admin.StackedInline):
    model = Users
    can_delete = False
    verbose_name_plural = "users"


class UserAdmin(BaseUserAdmin):
    inlines = (UsersInline,)

admin.site.unregister(User)
admin.site.register(Posts)
admin.site.register(User, UserAdmin)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Subscription)
admin.site.register(Notifications)
admin.site.register(Report)
