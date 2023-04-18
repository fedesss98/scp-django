from django.contrib import admin

# Register your models here.
from events.models import *

admin.site.register(Athlete)
admin.site.register(Club)
admin.site.register(Event)
admin.site.register(Race)
admin.site.register(Crew)

