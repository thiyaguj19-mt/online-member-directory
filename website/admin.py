from django.contrib import admin
from .models import *

# Register your models here.
#admin.site.register(Region)
#admin.site.register(Center)
admin.site.register(OrgRole)
#admin.site.register(AppRole)
#admin.site.register(Member)

class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(Region, RegionAdmin)

class AppRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'level')

admin.site.register(AppRole, AppRoleAdmin)

class CenterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'region')
    list_filter = ('region', 'name')

admin.site.register(Center, CenterAdmin)

class MemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'region', 'center', 'get_orgrole', 'approle')

admin.site.register(Member, MemberAdmin)
