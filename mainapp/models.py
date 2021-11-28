from django.conf import settings
from django.db import models
from django.utils import timezone


class User(models.Model):
    nickname = models.CharField(max_length=50, unique=True)
    photo = models.ImageField(max_length=200, blank=True, null=True)
    USER_ROLE_CHOICES = (
        (1, 'Watcher'),
        (2, 'Author'),
        (3, 'Admin'),
    )
    role = models.ForeignKey('Roles', max_length=1, choices=USER_ROLE_CHOICES, on_delete=models.SET_NULL, blank=True, null=True, default=1)
    bio = models.CharField(max_length=100, blank=True, null=True)
    age = models.PositiveIntegerField()
    telephone = models.PositiveIntegerField(unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(min_length=5, max_length=250)
    registration = models.DateTimeField(auto_now_add=True)
    last_entry = models.DateTimeField(auto_now=True)

    def new_last_entry(self):
        self.save()

    def __str__(self):
        return self.nickname + ', role: ' + str(self.role) + ', last entry: ' + str(self.last_entry)
