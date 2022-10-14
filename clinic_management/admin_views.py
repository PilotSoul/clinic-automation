from django.contrib import messages

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from clinic_management.models import CustomUser


def admin_home(request):
    return render(request, "admin_template/home_content.html")


def add_doctor(request):
    return render(request, "admin_template/add_doctor_template.html")


def add_doctor_save(request):
    if request.method != "POST":
        return HttpResponse("<h2> Method not allowed </h2>")
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        full_name = request.POST.get('full_name').split(" ")
        first_name = full_name[1]
        last_name = full_name[0]
        password = request.POST.get('password')
        try:
            user = CustomUser.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password, user_type=3)
            user.save()
            messages.success(request, "Yooohhoo!")
            return HttpResponseRedirect("/add_doctor")
        except Exception as e:
            print(e)
            messages.error(request, "Failed")
            return HttpResponseRedirect("/add_doctor")