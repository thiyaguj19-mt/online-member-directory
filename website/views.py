from django.shortcuts import render
from django.http import HttpResponse

# def index(request):
#     return HttpResponse("Hello World")

#This is the front home page screen view

def home(request):
    return render(request,'home.html',{}) 


#To import file - Admin Use   
def importFile(request):
    return render(request, 'import-page.html',{})   

#To export file - Admin Use  
def exportFile(request):
    return render(request, 'export-page.html',{})      
