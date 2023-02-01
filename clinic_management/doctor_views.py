from django.contrib import messages
from django.core.files.storage import FileSystemStorage

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from clinic_management.models import CustomUser, Consumable, Doctor, Service, Appointment, Patient, Staff
import uuid


def doctor_home(request):
    return render(request, "doctor_template/home_content.html")


def doctor_signup(request):
    return render(request, "doctor_template/signup_template.html")


def doctor_self(request, doctor_id):
    doctor = Doctor.objects.get(admin=doctor_id)
    return render(request, "doctor_template/edit_doctor_template.html", {"doctor":doctor})


def look_doctor_document(request, doctor_id):
    doctor = Doctor.objects.get(admin=doctor_id)
    return render(request, "doctor_template/look_doctor_template.html", {"doctor": doctor})


def doctor_calendar(request, doctor_id):
    doctor = Doctor.objects.get(admin=doctor_id)
    return render(request, "doctor_template/calendar_template.html", {"doctor": doctor})


def doctor_appointments(request, doctor_id):
    doctor = Doctor.objects.get(admin=doctor_id)
    return render(request, "doctor_template/doctor_appointments_template.html", {"doctor": doctor})


def edit_doctor_app(request, doctor_id):
    doctor = Doctor.objects.get(admin=doctor_id)
    return render(request, "doctor_template/edit_app_template.html", {"doctor": doctor})