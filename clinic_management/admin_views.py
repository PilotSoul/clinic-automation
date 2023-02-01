from django.contrib import messages
from django.core.files.storage import FileSystemStorage

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from clinic_management.models import CustomUser, Consumable, Doctor, Service, Appointment, Patient, Staff, DoctorDocument, PatientDocument, Consumable
import uuid
from clinic_management.documents_preparation.doc_by_doctor import document_by_doctor


def admin_home(request):
    return render(request, "admin_template/home_content.html")


def add_doctor(request):
    doctors = Doctor.objects.all()
    return render(request, "admin_template/add_doctor_template.html", {"doctors": doctors})


def add_doctor_save(request):
    is_success = True
    if request.method != "POST":
        return HttpResponse("<h2> Method not allowed </h2>")
    else:
        full_name = request.POST.get('full_name').split(" ")
        first_name = full_name[1]
        last_name = full_name[0]
        try:
            surname = full_name[2]
        except:
            surname = ""
        email = request.POST.get('email')
        birth_date = request.POST.get('birth_date')
        if request.POST.get('sex') == 'Мужчина':
            sex = 'м'
        else:
            sex = 'ж'
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        qualification = request.POST.get('qualification')
        password = request.POST.get('password')
        if address == "" or phone_number == "" or full_name == "":
            is_success = False
        try:
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save("avatars/"+profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        except:
            profile_pic_url = "/media/avatars/unAuth.png"
        if not is_success:
            messages.error(request, "Заполнено некорректно")
            return HttpResponseRedirect("/add_doctor")
        try:
            user = CustomUser.objects.create_user(
                username=uuid.uuid4().hex[:30],
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
                user_type=3)
            user.doctor.surname = surname
            user.doctor.birth_date = birth_date
            user.doctor.sex = sex
            user.doctor.address = address
            user.doctor.phone = phone_number
            user.doctor.qualification = qualification
            user.doctor.photo_path = profile_pic_url
            user.save()
            messages.success(request, "Пользователь успешно создан!")
            return HttpResponseRedirect("/add_doctor")
        except Exception as e:
            print(e)
            messages.error(request, "Заполнено некорректно")
            return HttpResponseRedirect("/add_doctor")


def add_consumable(request):
    consumables = Consumable.objects.all()
    return render(request, "admin_template/add_consumable_template.html", {"consumables": consumables})


def add_consumable_save(request):
    if request.method != "POST":
        return HttpResponse("<h2> Method not allowed </h2>")
    else:
        cons_name = request.POST.get('consumable')
        cons_amount = request.POST.get('amount')
        man_name = request.POST.get('manufacter')
        pack = request.POST.get('pack')
        cons_price = request.POST.get('price')
        if cons_price == "" or cons_name == "" or man_name == "" or cons_amount == "":
            messages.error(request, "Заполнено некорректно")
            return HttpResponseRedirect("/add_consumable")
        try:
            cons_model=Consumable(name=cons_name, manufacter=man_name, amount=cons_amount, pack=pack, price=cons_price)
            cons_model.save()
            messages.success(request, "Услуга успешно создана!")
            return HttpResponseRedirect("/add_consumable")
        except Exception as e:
            messages.error(request, "Заполнено некорректно")
            return HttpResponseRedirect("/add_consumable")


def add_service(request):
    services = Service.objects.all()
    return render(request, "admin_template/add_service_template.html", {"services": services})


def add_service_save(request):
    if request.method != "POST":
        return HttpResponse("<h2> Method not allowed </h2>")
    else:
        service_name = request.POST.get('service')
        service_price = request.POST.get('price')
        try:
            service_model=Service(name=service_name, price=service_price)
            service_model.save()
            messages.success(request, "Услуга успешно создана!")
            return HttpResponseRedirect("/add_service")
        except Exception as e:
            messages.error(request, "Заполнено некорректно")
            return HttpResponseRedirect("/add_service")


def edit_service(request, service_id):
    service=Service.objects.get(id=service_id)
    return render(request, "admin_template/edit_service_template.html", {"service":service})


def edit_service_save(request):
    if request.method != "POST":
        return HttpResponse("<h2> Method not allowed </h2>")
    else:
        service_id = request.POST.get("service_id")
        service_name = request.POST.get('service')
        service_price = request.POST.get('price')
        print(service_price)
        try:
            service_model = Service.objects.get(id=service_id)
            service_model.name = service_name
            service_model.price = service_price
            service_model.save()

            messages.success(request, "Информация об услуге успешно изменена!")
            return HttpResponseRedirect("/edit_service/" + service_id)
        except Exception as e:
            print(e)
            messages.error(request, "Заполнено некорректно")
            return HttpResponseRedirect("/edit_service/" + service_id)


def add_staff(request):
    staffs = Staff.objects.all()
    return render(request, "admin_template/add_staff_template.html", {"staffs": staffs})


def add_staff_save(request):
    if request.method != "POST":
        return HttpResponse("<h2> Method not allowed </h2>")
    else:
        full_name = request.POST.get('full_name').split(" ")
        first_name = full_name[1]
        last_name = full_name[0]
        try:
            surname = full_name[2]
        except:
            surname = ""
        email = request.POST.get('email')
        birth_date = request.POST.get('birth_date')
        if request.POST.get('sex') == 'Мужчина':
            sex = 'м'
        else:
            sex = 'ж'
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        password = request.POST.get('password')
        try:
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save("avatars/"+profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        except:
            profile_pic_url = "/media/avatars/unAuth.png"
        try:
            user = CustomUser.objects.create_user(
                username=uuid.uuid4().hex[:30],
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
                user_type=4)
            user.staff.surname = surname
            user.staff.birth_date = birth_date # "1985-05-04"
            user.staff.sex = sex
            user.staff.address = address
            user.staff.phone = phone_number
            user.staff.photo_path = profile_pic_url
            user.save()
            messages.success(request, "Пользователь успешно создан!")
            return HttpResponseRedirect("/add_staff")
        except Exception as e:
            print(e)
            messages.error(request, "Заполнено некорректно")
            return HttpResponseRedirect("/add_staff")


def edit_staff(request, staff_id):
    staff=Staff.objects.get(admin=staff_id)
    return render(request, "admin_template/edit_staff_template.html", {"staff":staff})


def edit_staff_save(request):
    if request.method != "POST":
        return HttpResponse("<h2> Method not allowed </h2>")
    else:
        staff_id = request.POST.get("staff_id")
        full_name = request.POST.get('full_name').split(" ")
        first_name = full_name[1]
        last_name = full_name[0]
        try:
            surname = full_name[2]
        except:
            surname = ""
        email = request.POST.get('email')
        birth_date = request.POST.get('birth_date')
        if request.POST.get('sex') == 'Мужчина':
            sex = 'м'
        else:
            sex = 'ж'
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        if request.FILES.get('profile_pic', False):
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save("avatars/" + profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None
        try:
            user = CustomUser.objects.get(id=staff_id)
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            patient_model = Staff.objects.get(admin=staff_id)
            patient_model.surname = surname
            patient_model.birth_date = birth_date
            patient_model.sex = sex
            patient_model.address = address
            patient_model.phone = phone_number
            if profile_pic_url is not None:
                patient_model.photo_path = profile_pic_url
            patient_model.save()
            messages.success(request, "Информация о менеджере успешно изменена!")
            return HttpResponseRedirect("/edit_patient/" + staff_id)
        except Exception as e:
            print(e)
            messages.error(request, "Заполнено некорректно")
            return HttpResponseRedirect("/edit_patient/" + staff_id)


def add_patient(request):
    patients = Patient.objects.all()
    return render(request, "admin_template/add_patient_template.html", {"patients": patients})


def add_patient_save(request):
    is_success = True
    if request.method != "POST":
        return HttpResponse("<h2> Method not allowed </h2>")
    else:
        full_name = request.POST.get('full_name').split(" ")
        first_name = full_name[1]
        last_name = full_name[0]
        try:
            surname = full_name[2]
        except:
            surname = ""
        email = request.POST.get('email')
        birth_date = request.POST.get('birth_date')
        if request.POST.get('sex') == 'Мужчина':
            sex = 'м'
        else:
            sex = 'ж'
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        password = request.POST.get('password')
        try:
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save("avatars/"+profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        except:
            profile_pic_url = "/media/avatars/unAuth.png"
        if not is_success:
            messages.error(request, "Заполнено некорректно")
            return HttpResponseRedirect("/add_patient")
        try:
            user = CustomUser.objects.create_user(
                username=uuid.uuid4().hex[:30],
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
                user_type=2)
            user.patient.surname = surname
            user.patient.birth_date = birth_date # "1985-05-04"
            user.patient.sex = sex
            user.patient.address = address
            user.patient.phone = phone_number
            user.patient.photo_path = profile_pic_url
            user.save()
            messages.success(request, "Пользователь успешно создан!")
            return HttpResponseRedirect("/add_patient")
        except Exception as e:
            print(e)
            messages.error(request, "Заполнено некорректно")
            return HttpResponseRedirect("/add_patient")


def edit_patient(request, patient_id):
    patient=Patient.objects.get(admin=patient_id)
    return render(request, "admin_template/edit_patient_template.html", {"patient":patient})


def edit_patient_save(request):
    is_success = True
    if request.method != "POST":
        return HttpResponse("<h2> Method not allowed </h2>")
    else:
        patient_id = request.POST.get("patient_id")
        full_name = request.POST.get('full_name').split(" ")
        first_name = full_name[1]
        last_name = full_name[0]
        try:
            surname = full_name[2]
        except:
            surname = ""
        email = request.POST.get('email')
        birth_date = request.POST.get('birth_date')
        if request.POST.get('sex') == 'Мужчина':
            sex = 'м'
        else:
            sex = 'ж'
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        if address == "" or phone_number == "" or full_name == "":
            is_success = False
        if request.FILES.get('profile_pic', False):
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save("avatars/" + profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None
        if not is_success:
            messages.error(request, "Заполнено некорректно")
            return HttpResponseRedirect("/edit_patient/" + patient_id)
        try:
            user = CustomUser.objects.get(id=patient_id)
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            patient_model = Patient.objects.get(admin=patient_id)
            patient_model.surname = surname
            patient_model.birth_date = birth_date
            patient_model.sex = sex
            patient_model.address = address
            patient_model.phone = phone_number
            if profile_pic_url is not None:
                patient_model.photo_path = profile_pic_url
            patient_model.save()
            messages.success(request, "Информация о пациенте успешно изменена!")
            return HttpResponseRedirect("/edit_patient/" + patient_id)
        except Exception as e:
            print(e)
            messages.error(request, "Заполнено некорректно")
            return HttpResponseRedirect("/edit_patient/" + patient_id)


def delete_patient(request, patient_id):
    if request.method != "POST":
        return HttpResponse("<h2> Method not allowed </h2>")
    else:
        if request.POST.get('action') == 'No':
            return HttpResponseRedirect("/edit_patient/" + patient_id)
        elif request.POST.get('action') == 'Yes':
            try:
                appointment = Appointment.objects.filter(id_patient=Patient.objects.get(admin=patient_id))
                appointment.delete()
                user = CustomUser.objects.get(id=patient_id)
                user.delete()

                return HttpResponseRedirect("/add_patient/")
            except Exception as e:
                print(e)
                messages.error(request, "Заполнено некорректно")
                return HttpResponseRedirect("/add_patient/")


def edit_doctor(request, doctor_id):
    doctor=Doctor.objects.get(admin=doctor_id)
    return render(request, "admin_template/edit_doctor_template.html", {"doctor":doctor})


def edit_doctor_save(request):
    is_success = True
    if request.method != "POST":
        return HttpResponse("<h2> Method not allowed </h2>")
    else:
        doctor_id = request.POST.get("doctor_id")
        full_name = request.POST.get('full_name').split(" ")
        first_name = full_name[1]
        last_name = full_name[0]
        try:
            surname = full_name[2]
        except:
            surname = ""
        email = request.POST.get('email')
        birth_date = request.POST.get('birth_date')
        if request.POST.get('sex') == 'Мужчина':
            sex = 'м'
        else:
            sex = 'ж'
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        qualification = request.POST.get('qualification')
        if address == "" or email == "" or full_name == "" or phone_number == "":
            is_success = False
        if request.FILES.get('profile_pic', False):
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save("avatars/"+profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None
        if not is_success:
            messages.error(request, "Заполнено некорректно")
            return HttpResponseRedirect("/edit_doctor/"+doctor_id)
        try:
            user = CustomUser.objects.get(id=doctor_id)
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            doctor_model = Doctor.objects.get(admin=doctor_id)
            doctor_model.surname = surname
            doctor_model.birth_date = birth_date
            doctor_model.sex = sex
            doctor_model.address = address
            doctor_model.phone = phone_number
            doctor_model.qualification = qualification
            if profile_pic_url is not None:
                doctor_model.photo_path = profile_pic_url
            doctor_model.save()

            messages.success(request, "Информация о враче успешно изменена!")
            return HttpResponseRedirect("/edit_doctor/"+doctor_id)
        except Exception as e:
            print(e)
            messages.error(request, "Заполнено некорректно")
            return HttpResponseRedirect("/edit_doctor/"+doctor_id)


def delete_doctor(request, doctor_id):
    if request.method != "POST":
        return HttpResponse("<h2> Method not allowed </h2>")
    else:
        if request.POST.get('action') == 'No':
            return HttpResponseRedirect("/edit_doctor/" + doctor_id)
        elif request.POST.get('action') == 'Yes':
            # doctor_id = request.POST.get("doctor_id")
            try:
                user = CustomUser.objects.get(id=doctor_id)
                user.delete()

                return HttpResponseRedirect("/add_doctor/")
            except Exception as e:
                print(e)
                messages.error(request, "Заполнено некорректно")
                return HttpResponseRedirect("/add_doctor/")


def form_c(request):
    return render(request, "admin_template/form_template.html")


def delete_service(request, service_id):
    if request.method != "POST":
        return HttpResponse("<h2> Method not allowed </h2>")
    else:
        if request.POST.get('action') == 'No':
            return HttpResponseRedirect("/edit_service/" + service_id)
        elif request.POST.get('action') == 'Yes':
            # doctor_id = request.POST.get("doctor_id")
            try:
                service = Service.objects.get(id=service_id)
                service.delete()

                return HttpResponseRedirect("/add_service/")
            except Exception as e:
                print(e)
                messages.error(request, "Заполнено некорректно")
                return HttpResponseRedirect("/add_service/")


def look_documents(request):
    doctors_documents = DoctorDocument.objects.all()
    patient_documents = PatientDocument.objects.all()
    # patient = Patient.objects.get(id=patient_documents.id_patient)
    # doctor = Doctor.objects.get(id=doctors_documents.id_doctor)
    return render(request, "admin_template/documents_template.html", {"doctors_document": doctors_documents, "patients_document": patient_documents})
    #должен быть выбор периода и врача и за этот период выбирается, какие услуги сделал врач и их итоговая стоимость


def create_document(request):
    doctors = Doctor.objects.all()
    return render(request, "admin_template/create_document_template.html", {"doctors": doctors})
    #должен быть выбор периода и врача и за этот период выбирается, какие услуги сделал врач и их итоговая стоимость


def create_document_save(request):
    if request.method != "POST":
        return HttpResponse("<h2> Method not allowed </h2>")
    else:
        doctor_id = request.POST.get('doctor')
        start_date = request.POST.get('start_date')
        finish_date = request.POST.get('finish_date')
        buf = document_by_doctor(doctor_id, start_date, finish_date)

        return FileResponse(buf, as_attachment=True, filename='doctor.xlsx')


def create_consumable(request):
    try:
        cons = Consumable.objects.create(name='Аппликаторы', manufacter='Dispodent', amount=100, pack='шт', price=155)
        cons.save()
        cons = Consumable.objects.create(name='Воск базисный', manufacter='Стома', amount=500, pack='г', price=1500)
        cons.save()
        cons = Consumable.objects.create(name='Дентин паста', manufacter='ВладМиВа', amount=50, pack='г', price=135)
        cons.save()
        return HttpResponse("<h2> Succeed </h2>")
    except Exception as e:
        print(e)
        return HttpResponse("<h2> Nooooo( </h2>")


def create_service(request):
    try:
        service = Service.objects.create(name='Чистка зубов', price=1900)
        service.consumable_name.set([2, 3, 5])
        service.save()
        return HttpResponse("<h2> Succeed </h2>")
    except Exception as e:
        print(e)
        return HttpResponse("<h2> Nooooo( </h2>")


def show_users(request):
    doctors, num_d = Doctor.objects.all(), Doctor.objects.count()
    patients, num_p  = Patient.objects.all(), Patient.objects.count()
    staffs, num_s = Staff.objects.all(), Staff.objects.count()
    res = num_s + num_p + num_d
    return render(request, "admin_template/users_template.html", {"doctors": doctors, "patients": patients, "staffs": staffs, "res": res})

def create_doctor_document(request):
    try:
        doc = DoctorDocument.objects.create(id_doctor=Doctor.objects.get(id=1), name="Отчет за 10.08.2019 - 20.10.2021")
        doc.save()
        doc = DoctorDocument.objects.create(id_doctor=Doctor.objects.get(id=1), name="Отчет за 11.09.2020 - 20.04.2022")
        doc.save()
        doc = DoctorDocument.objects.create(id_doctor=Doctor.objects.get(id=2), name="Отчет за 23.01.2020 - 15.08.2021")
        doc.save()
        doc = DoctorDocument.objects.create(id_doctor=Doctor.objects.get(id=2), name="Отчет за 01.01.2022 - 02.03.2022")
        doc.save()
        return HttpResponse("<h2> Succeed </h2>")
    except Exception as e:
        print(e)
        return HttpResponse("<h2> Nooooo( </h2>")


def create_patient_document(request):
    try:
        pat = PatientDocument.objects.create(id_patient=Patient.objects.get(id=7), name="Паспортные данные")
        pat.save()
        pat = PatientDocument.objects.create(id_patient=Patient.objects.get(id=9), name="Индивидуальный план лечения")
        pat.save()
        pat = PatientDocument.objects.create(id_patient=Patient.objects.get(id=9), name="Паспортные данные")
        pat.save()
        pat = PatientDocument.objects.create(id_patient=Patient.objects.get(id=2), name="Снимок КТ")
        pat.save()
        return HttpResponse("<h2> Succeed </h2>")
    except Exception as e:
        print(e)
        return HttpResponse("<h2> Nooooo( </h2>")


def create_appointment(request):
    try:
        appoint = Appointment.objects.create(id_doctor=Doctor.objects.get(id=1), id_patient=Patient.objects.get(id=5),  date_appointment='2022-12-01 20:00', is_finished=True, comment="")
        appoint.services.set([6, 7])
        appoint.save()
        return HttpResponse("<h2> Succeed </h2>")
    except Exception as e:
        print(e)
        return HttpResponse("<h2> Nooooo( </h2>")


def add_schedule(request):
    return render(request, "admin_template/add_schedule_template.html")