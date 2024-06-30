import os

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Таблица "Статусы"
class Statuses (models.Model):
   status_name = models.CharField(max_length=50, blank=False)

   def __str__(self):
    return  self.status_name

# Таблица "Приоритеты"
class Priorities (models.Model):
    priority_name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.priority_name


# Таблица "Подразделения"
class Divisions (models.Model):
    division_name = models.CharField(max_length=150, blank=False)

    def __str__(self):
        return self.division_name


# Таблица "Должности"
class Jobs (models.Model):
    job_name = models.CharField(max_length=150, blank=False)
    division = models.ForeignKey(Divisions, on_delete=models.CASCADE)

    def __str__(self):
        return self.job_name


# Таблица "Сотрудники"
class Profile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patron = models.CharField(max_length=100)
    job = models.ForeignKey(Jobs, blank=True, default='', null=True, on_delete=models.CASCADE)
    phone = models.CharField(blank=True, max_length=40)
    picture = models.ImageField(blank=True, null=True, upload_to='avatars/', default='avatars/default_profile.jpg')

    def __str__(self):
        return self.patron

# Таблица "Заявки"
class Requests (models.Model):
    request_date = models.DateTimeField(blank=True, null=True, default=timezone.now, editable=False)
    issued_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_creator', blank=True, null=True)
    request_name = models.CharField(max_length=150, blank=False)
    request_description = models.TextField(default=None)
    responsible = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='%(class)s_worker')
    priority = models.ForeignKey(Priorities, blank=False, on_delete=models.CASCADE)
    status = models.ForeignKey(Statuses, on_delete=models.CASCADE, blank=True, null=True)
    desired_date = models.DateTimeField(blank=False, null=True)
    attachment = models.FileField(blank=True, null=True, upload_to='user_files/')
    commentary = models.TextField(blank=True, null=True)
    delete_commentary = models.TextField(blank=True, null=True)
    revision_commentary = models.TextField(blank=True, null=True)
    responce_attachments = models.FileField(blank=True, null=True, upload_to='user_files/')
    date_completed = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.request_name


class Hardware (models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class IP_map (models.Model):
    ip_adress = models.GenericIPAddressField()
    mac_adress = models.CharField(max_length=100, blank=True, null=True,)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, default='', null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    hardware = models.ForeignKey(Hardware, on_delete=models.CASCADE, blank=True, default='', null=True)
    def __str__(self):
        return self.ip_adress

class Resourse_types (models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class LogPass (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, default='', null=True)
    resource = models.ForeignKey(Resourse_types, on_delete=models.CASCADE, blank=True, default='', null=True)
    login = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    extra_info = models.CharField(max_length=200, blank=True, null=True, default='')

    def __str__(self):
        return self.login

class Suppliers (models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Customs (models.Model):
    date = models.DateTimeField(blank=True, default='', null=True)
    supplier = models.ForeignKey(Suppliers, on_delete=models.CASCADE, blank=True, default='', null=True)
    summ = models.IntegerField(blank=True, default='', null=True)
    contents = models.TextField(blank=True, default='', null=True)

    def __str__(self):
        return self.summ