from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    classdict = {'class1':'CMSC136'}
    return render(request, 'app/index.html', classdict)
