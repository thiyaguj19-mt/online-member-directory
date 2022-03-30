from django.contrib import admin
from .models import *

# Register your models here.
#admin.site.register(Region)
#admin.site.register(Center)
#admin.site.register(OrgRole)
#admin.site.register(AppRole)
#admin.site.register(Member)
admin.site.register(Quotes)

class OrgRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(OrgRole, OrgRoleAdmin)

class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(Region, RegionAdmin)

class AppRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'level')

admin.site.register(AppRole, AppRoleAdmin)

class CenterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'region', 'status', 'center_type')
    list_filter = ('region', 'status', 'center_type', 'name')

admin.site.register(Center, CenterAdmin)

class MemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'region', 'center', 'get_orgrole', 'approle')
    list_filter = ('region', 'member_status', 'orgrole__name')

admin.site.register(Member, MemberAdmin)

class MetadataAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')

admin.site.register(Metadata, MetadataAdmin)

admin.site.site_header = 'Officers Portal'