from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('import-page/', views.importFile, name='import-page'),
    path('export-page/', views.exportFile, name='export-page')
]
