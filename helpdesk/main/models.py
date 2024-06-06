from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    phone = models.CharField(blank=True, max_length=20)
    picture = models.ImageField(blank=True, null=True, upload_to='avatars/', default='avatars/default_profile.jpg')

    def __str__(self):
        return self.patron

    # Сигналы на автоматическое обновление таблицы при создании или изменении данных пользователя
    '''
    @receiver(post_save, sender=User)
    def new_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
    '''

# Таблица "Заявки"
class Requests (models.Model):
    request_date = models.DateTimeField(blank=False)
    issued_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_creator')
    request_name = models.CharField(max_length=150, blank=False)
    request_description = models.TextField(default=None)
    responsible = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='%(class)s_worker')
    priority = models.ForeignKey(Priorities, blank=False, on_delete=models.CASCADE)
    status = models.ForeignKey(Statuses, blank=False, on_delete=models.CASCADE)
    desired_date = models.DateField(blank=True, null=True)
    attachment = models.FileField(blank=True, null=True, upload_to='user_files/')
    commentary = models.TextField(blank=True, null=True)
    delete_commentary = models.TextField(blank=True, null=True)
    revision_commentary = models.TextField(blank=True, null=True)
    date_completed = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.request_name
