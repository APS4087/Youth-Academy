from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ph_number = models.CharField(max_length=20)
    address = models.CharField(max_length=150)
    user_type = models.CharField(
        max_length=10,
        choices=[
            ('admin', 'Admin'),
            ('student', 'Student'),
            ('teacher', 'Teacher')]
    )

    def __str__(self):
        return self.user.username

