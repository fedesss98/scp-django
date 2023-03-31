from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from fantapoma.models import *


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class PlayerInline(admin.StackedInline):
    model = Player
    can_delete = False


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (PlayerInline,)


# Register your models here.
admin.site.register(Athlete)
admin.site.register(Special)
admin.site.register(Player)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
