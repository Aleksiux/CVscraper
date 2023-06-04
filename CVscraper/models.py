from django.db import models
from django.contrib.auth.admin import User


class CvForm(models.Model):
    cv_id = models.AutoField(primary_key=True)
    logo_url = models.CharField(max_length=3000)
    position = models.CharField(max_length=100)
    employer = models.CharField(max_length=20)
    salary = models.CharField(max_length=50)
    salary_taxes = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    how_old_ad = models.CharField(max_length=50)
    ad_link = models.CharField(max_length=3000)

    def __str__(self):
        return f"Position:{self.position} | employer: {self.employer}"


class Profile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    likes = models.ForeignKey(CvForm, on_delete=models.DO_NOTHING, related_name='likes')
