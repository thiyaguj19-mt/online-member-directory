from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('import', views.importFile, name = 'import-page'),
    path('export', views.exportFile, name = 'export-page'),
    path('national-officers', views.getAllNationalOfficers, name = 'national-officers-page'),
    path('regional-officers', views.getAllRegionalOfficers, name = 'regional-officers-page'),
    path('center-officers', views.getAllCenterOfficers, name = 'center-officers-page'),
    path('search_members', views.search_members, name = 'search-members'),
    path('region_role/<int:regionId>', views.getRegionOfficers, name = 'region-page'),
    path('center_role/<int:centerId>', views.getCenterOfficers, name = 'center-page'),
    path('getCenterOfficers/<int:centerId>', views.getCenterOfficers, name = 'centerOfficers'),
    path('getRegionalCenters/<int:regionId>', views.getRegionalCenters, name = 'regionalCenters'),
    path('uploadFile', views.uploadFile, name = 'uploadFile'),
]
