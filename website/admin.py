from django.contrib import admin
from .models import *

# Register your models here.
#admin.site.register(Region)
#admin.site.register(Center)
admin.site.register(OrgRole)
admin.site.register(AppRole)
admin.site.register(Member)

class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(Region, RegionAdmin)

class CenterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'region')

admin.site.register(Center, CenterAdmin)
