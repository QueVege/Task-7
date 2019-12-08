from django.db import models
from django.conf import settings
from django.utils import timezone


class Company(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'company {self.name}'


class Manager(models.Model):
    company = models.ForeignKey(
        Company, related_name='managers', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    def __str__(self):
        return f'manager {self.first_name} {self.last_name} at {self.company}'


class Work(models.Model):
    initiator = models.ForeignKey(
        Manager, related_name='works', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'work {self.name}'

class Worker(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    def __str__(self):
        return f'worker {self.first_name} {self.last_name}'

class WorkPlace(models.Model):
    work = models.ForeignKey(
        Work, related_name='workplaces', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    worker = models.ForeignKey(
        Worker, related_name='workplaces', on_delete=models.CASCADE)

    NEW = 0
    APPROVED = 1
    CANCELLED = 2
    FINISHED = 3

    STATUS_CHOICES = (
        (NEW, 'New'),
        (APPROVED, 'Approved'),
        (CANCELLED, 'Cancelled'),
        (FINISHED, 'Finished'),
    )

    status = models.IntegerField(choices=STATUS_CHOICES, default=NEW)

    def __str__(self):
        return f'workplace {self.name}'

class WorkTime(models.Model):
    NEW = 0
    APPROVED = 1
    CANCELLED = 2

    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    
    worker = models.ForeignKey(
        Worker, related_name='worktimes', on_delete=models.CASCADE)
    workplace = models.ForeignKey(
        WorkPlace, on_delete=models.CASCADE)


    STATUS_CHOICES = (
        (NEW, 'New'),
        (APPROVED, 'Approved'),
        (CANCELLED, 'Cancelled'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=NEW)

