from django.contrib.auth.models import User
from django.db import models




class Student(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=False)
    phone = models.CharField(max_length=200, null=False)
    email = models.CharField(max_length=200, null=False, unique=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        if self.user == None:
            return "ERROR-Student name is null"
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=200, unique=True)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    content = models.TextField()
    link= models.TextField()

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return str(self.pk)+" "+self.title



