from django.db import models
from django.contrib.auth.admin import User
from PIL import Image


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
    work_area = models.CharField(max_length=50)

    def __str__(self):
        return f"Position:{self.position} | employer: {self.employer} | city: {self.city} |"


class Profile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    likes = models.ManyToManyField(CvForm, related_name='likes')
    photo = models.ImageField(default="profile_pics/default.png", upload_to="profile_pics")

    def save(self, *args, **kwargs):
        """ Run the usual save function but also resize uploaded photo        """
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)
        # if img.height > 300 or img.width > 300:
        output_size = (300, 300)
        img.thumbnail(output_size)
        img.save(self.photo.path)