from django.shortcuts import render
from django.http import HttpResponse

# def index(request):
#     return HttpResponse("Hello World")

#This is the front home page screen view

def home(request):
    return render(request,'home.html',{})    
