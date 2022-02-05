from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('import', views.importFile, name = 'import-page'),
    path('export', views.exportFile, name = 'export-page'),
]
