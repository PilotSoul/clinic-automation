from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    user_type_data = ((1, "Administrator"), (2, "Patient"), (3, "Doctor"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=14)


class AdminClinic(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class Patient(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class Doctor(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminClinic.objects.create(admin=instance)
        elif instance.user_type == 2:
            Patient.objects.create(admin=instance)
        elif instance.user_type == 3:
            Doctor.objects.create(admin=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminclinic.save()
    elif instance.user_type == 2:
        instance.patient.save()
    elif instance.user_type == 3:
        instance.doctor.save()