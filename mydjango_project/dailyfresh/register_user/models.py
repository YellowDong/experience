from django.db import models


class UserInfo(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=40)
    email = models.CharField(max_length=20)
    reseiver = models.CharField(max_length=20, default='')
    address = models.CharField(max_length=100, default='')
    phonenum = models.CharField(max_length=11, default='')
    zip_code = models.CharField(max_length=6, default='')