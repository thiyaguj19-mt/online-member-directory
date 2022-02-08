from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('import', views.importFile, name = 'import-page'),
    path('export', views.exportFile, name = 'export-page'),
    path('search_members', views.search_members, name = 'search-members'),
    path('region_role/<int:regionId>', views.getRegionOfficers, name = 'region-page'),
    path('uploadFile', views.uploadFile, name = 'uploadFile'),
]
