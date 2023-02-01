from django.contrib import messages
from django.core.files.storage import FileSystemStorage

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from clinic_management.models import CustomUser, Consumable, Doctor, Service, Appointment, Patient, Staff
import uuid


def patient_home(request):
    return render(request, "patient_template/home_content.html")


def patient_signup(request):
    return render(request, "patient_template/signup_template.html")


def patient_appointments(request):
    return render(request, "patient_template/appointments_template.html")


def patient_self(request, patient_id):
    patient = Patient.objects.get(admin=patient_id)
    return render(request, "patient_template/edit_patient_template.html", {"patient":patient})


def look_patient_document(request, patient_id):
    patient = Patient.objects.get(admin=patient_id)
    return render(request, "patient_template/look_patient_template.html", {"patient": patient})