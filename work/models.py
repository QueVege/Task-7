from django.db import models
from django.conf import settings
from django.utils import timezone


class Company(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'company {self.name}'


class Manager(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    def __str__(self):
        return f'manager {self.first_name} {self.last_name} at {self.company}'


class Work(models.Model):
    initiator = models.ForeignKey(Manager, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'work {self.name}'

    
class Worker(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    def __str__(self):
        return f'worker {self.first_name} {self.last_name}'

    
class Position(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    worker = models.OneToOneField(Worker, on_delete=models.CASCADE)

    def __str__(self):
        return f'position {self.name}'
