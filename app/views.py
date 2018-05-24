from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import requests
import csv


def login(request):
    if request.method == 'POST':
        name = request.POST['name']
        password = request.POST['password']
        if CheckIfUserAlreadyRegistered(name, password):
            return render(request, 'app/home.html')
        else:
            CreateUserInDB(name, password)
            return render(request, 'app/home.html')
    else:
        return render(request, 'app/login.html')


def CheckIfUserAlreadyRegistered(name, password):
    return True


def CreateUserInDB(name, password):
    return True
