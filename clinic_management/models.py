from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

sex_type = ((1, "Woman"), (2, "Man"))


class CustomUser(AbstractUser):
    global sex_type
    user_type_data = ((1, "Admin"), (2, "Patient"), (3, "Doctor"), (4, "Staff"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=14)


class AdminClinic(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class Patient(models.Model):
    global sex_type
    id=models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    sex = models.CharField(default=1, choices=sex_type, max_length=6)
    surname = models.CharField(max_length=255, null=True)
    birth_date = models.DateField(null=True)
    address=models.CharField(max_length=255)
    phone=models.CharField(max_length=50)
    photo_path=models.ImageField(upload_to ='avatars/', default ='unAuth.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class Doctor(models.Model):
    global sex_type
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    sex = models.CharField(default=1, choices=sex_type, max_length=6)
    surname=models.CharField(max_length=255, null=True)
    birth_date=models.DateField(null=True)
    address=models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    qualification=models.CharField(max_length=255, null=True)
    experience=models.IntegerField(null=True)
    # change default
    photo_path=models.ImageField(upload_to ='avatars/', default = 'unAuth.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class Staff(models.Model):
    global sex_type
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    sex = models.CharField(default=1, choices=sex_type, max_length=6)
    surname = models.CharField(max_length=255, null=True)
    birth_date = models.DateField(null=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    photo_path = models.ImageField(upload_to='avatars/', default='unAuth.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class DoctorDocument(models.Model):
    id_doctor=models.ForeignKey(Doctor, on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    document_path = models.FileField(upload_to='documents/')
    objects = models.Manager()


class PatientDocument(models.Model):
    id_patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    document_path=models.FileField(upload_to='documents/')
    objects = models.Manager()


class Consumable(models.Model):
    pack_type=((1, 'шт'), (2, 'л'), (3, 'г'), (4, 'мг'), (5, 'кг'))
    name=models.CharField(max_length=255)
    amount=models.IntegerField()
    manufacter=models.CharField(max_length=255)
    pack=models.CharField(default='3', choices=pack_type, max_length=6)
    price=models.FloatField()
    ed_price=models.CharField(default="руб", max_length=255)
    objects = models.Manager()


class Service(models.Model):
    name=models.CharField(max_length=255)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    consumable_name = models.ManyToManyField(Consumable, blank=True, symmetrical=False)
    objects = models.Manager()


class Appointment(models.Model):
    id_doctor=models.ForeignKey(Doctor, on_delete=models.CASCADE)
    id_patient=models.ForeignKey(Patient, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service, blank=True, symmetrical=False)
    date_appointment=models.DateTimeField()
    is_finished=models.BooleanField(default=False)
    comment=models.CharField(max_length=255)
    objects = models.Manager()


class DateAppointment(models.Model):
    date_appointment = models.DateTimeField()
    id_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    id_appointment=models.ForeignKey(Appointment, on_delete=models.SET_NULL, blank=True, null=True)
    objects = models.Manager()


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminClinic.objects.create(admin=instance)
        elif instance.user_type == 2:
            Patient.objects.create(admin=instance, sex=1, surname="", birth_date="1900-01-01", address="", phone="", photo_path="unAuth.png")
        elif instance.user_type == 3:
            Doctor.objects.create(admin=instance, sex=1, surname="", birth_date="1900-01-01", address="", phone="", qualification="", experience=0, photo_path="unAuth.png")
        elif instance.user_type == 4:
            Staff.objects.create(admin=instance, sex=1, surname="", birth_date="1900-01-01", address="", phone="", photo_path="unAuth.png")


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminclinic.save()
    elif instance.user_type == 2:
        instance.patient.save()
    elif instance.user_type == 3:
        instance.doctor.save()
    elif instance.user_type == 4:
        instance.staff.save()