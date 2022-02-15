from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('import', views.importFile, name = 'import-page'),
    path('export', views.exportFile, name = 'export-page'),
    path('search_members', views.search_members, name = 'search-members'),
    
    path('role-filter-list', views.role_filter_list, name='role-filter-list'),
    path('national-officers', views.getAllNationalOfficers, name = 'national-officers-page'),
    path('regional-officers', views.getAllRegionalOfficers, name = 'regional-officers-page'),
    path('center-officers', views.getAllCenterOfficers, name = 'center-officers-page'),
    path('region_role/<int:regionId>', views.getRegionOfficers, name = 'region-page'),
    path('center_role/<int:centerId>', views.getCenterOfficers, name = 'center-page'),
    path('center-names-all', views.getallCenters, name = 'center-names-all'),
    path('region-names-all', views.getAllRegions, name = 'region-names-all'),
    path('show-rcenters/<int:regionId>', views.getRegionalCenters, name = 'show-rcenters'),
    path('uploadFile', views.uploadFile, name = 'uploadFile'),
]
