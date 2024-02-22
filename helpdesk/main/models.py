from django.db import models

# Таблица "Статусы"
class Statuses (models.Model):
   status_name = models.CharField(max_length=50, blank=False)
   class Meta:
       db_table = 'Statuses'

   def __str__(self):
    return  self.status_name

# Таблица "Приоритеты"
class Priorities (models.Model):
    priority_name = models.CharField(max_length=50, blank=False)

    class Meta:
        db_table = 'Priorities'

    def __str__(self):
        return self.priority_name


# Таблица "Подразделения"
class Divisions (models.Model):
    division_name = models.CharField(max_length=150, blank=False)

    class Meta:
        db_table = 'Divisions'

    def __str__(self):
        return self.division_name


# Таблица "Должности"
class Jobs (models.Model):
    job_name = models.CharField(max_length=150, blank=False)
    division = models.ForeignKey(Divisions, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Jobs'

    def __str__(self):
        return self.job_name


# Таблица "Сотрудники"
class Workers (models.Model):
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    patronymic = models.CharField(max_length=100)
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    email = models.EmailField()

    class Meta:
        db_table = 'Workers'

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'


# Таблица "Заявки"
class Requests (models.Model):
    request_date = models.DateTimeField(blank=False)
    issued_by = models.ForeignKey(Workers, on_delete=models.CASCADE, related_name='%(class)s_creator')
    request_name = models.CharField(max_length=150, blank=False)
    request_description = models.TextField()
    responsible = models.ForeignKey(Workers, blank=False, on_delete=models.CASCADE, related_name='%(class)s_worker')
    priority = models.ForeignKey(Priorities, blank=False, on_delete=models.CASCADE)
    status = models.ForeignKey(Statuses, blank=False, on_delete=models.CASCADE)
    date_completed = models.DateTimeField()

    class Meta:
        db_table = 'Requests'

    def __str__(self):
        return self.request_name
