from django.urls import path
from . import views
from django.conf.urls import url, include

urlpatterns = [
    path('', views.home, name='home'),
    path('import', views.importFile, name = 'import-page'),
    path('export', views.exportFile, name = 'export-page'),
    path('usa_regionsmap', views.getUSARegionsMap, name ='usa_regionsmap'),
    path('user', views.showUserProfile, name = 'user-page'),
    path('national-officers', views.getAllNationalOfficers, name = 'national-officers-page'),
    path('regional-officers', views.getAllRegionalOfficers, name = 'regional-officers-page'),
    path('center-officers', views.getAllCenterOfficers, name = 'center-officers-page'),
    path('search_members', views.search_members, name = 'search-members'),
    path('region_role/<int:regionId>', views.getRegionOfficers, name = 'region-page'),
    path('center_role/<int:centerId>', views.getCenterOfficers, name = 'center-page'),
    path('getCenterOfficers/<int:centerId>', views.getCenterOfficers, name = 'centerOfficers'),
    path('getRegionalCenters/<int:regionId>', views.getRegionalCenters, name = 'regionalCenters'),
    path('uploadFile', views.uploadFile, name = 'uploadFile'),
    path('region/<int:regionId>/centers', views.displayRegionCenters, name= 'region-centers'),
    path('contactus', views.contactus, name = 'contactus'),
    path('center/<int:centerId>/members', views.getMembersForCenter, name= 'center-members'),
    path('getMemberData/', views.getMemberData, name='memberData'),
    path('updateMemberProfile/', views.updateMemberProfile, name='updateMemberProfile'),
    path('updateMemberStatus/', views.updateMemberStatus, name='updateMemberStatus'),
    path('enableNotification/', views.enableNotification, name='enableNotification'),
]

urlpatterns += [
    url(r'^swingtime/', include('swingtime.urls')),
]
