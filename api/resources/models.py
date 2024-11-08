from django.contrib.auth.models import User
from django.db import models

class UserAuthority(models.Model):
    ROLE_CHOICES = [
        ("admin", "管理者"),
        ("staff", "一般ユーザー"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="staff")
