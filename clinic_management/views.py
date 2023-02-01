from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from clinic_management.EmailBackend import EmailBackend


def showDemoPage(request):
    return render(request, "demo.html")


def showLoginPage(request):
    return render(request, "login.html")


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2> Method not allowed </h2>")
    else:
        user = EmailBackend.authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
        if user is not None:
            login(request, user)
            if user.user_type=='1':
                return HttpResponseRedirect(reverse("admin_home"))
            elif user.user_type=='2':
                return HttpResponseRedirect(reverse("patient_home"))
            elif user.user_type=='3':
                return HttpResponseRedirect(reverse("doctor_home"))
        else:
            messages.error(request, "Логин или пароль введены неверно")
            return HttpResponseRedirect("/")


def getUserDetails(request):
    if request.user is not None:
        return HttpResponse("User: " + request.user.email + " usertype: " + request.user.user_type)
    else:
        return HttpResponse("<h2> Пожалуйста войдите или зарегистрируйтесь</h2>")


def logoutUser(request):
    logout(request)
    return HttpResponseRedirect("/")