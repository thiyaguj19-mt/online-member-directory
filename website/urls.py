from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('import', views.importFile, name = 'import-page'),
    path('export', views.exportFile, name = 'export-page'),
    path('search_members', views.search_members, name = 'search-members'),
    path('region_role/<int:regionId>', views.getRegionOfficers, name = 'region-page'),
    path('center_role/<int:centerId>', views.getCenterOfficers, name = 'center-page'),
    path('getCenterOfficers/<int:centerId>', views.getCenterOfficers, name = 'centerOfficers'),
    path('getRegionalCenters/<int:regionId>', views.getRegionalCenters, name = 'regionalCenters'),
    path('uploadFile', views.uploadFile, name = 'uploadFile'),
]
