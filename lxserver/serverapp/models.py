from django.db import models

# Create your models here.
class User_profile(models.Model):

    class Meta:
        app_label = 'serverapp'

    name = models.CharField(max_length=20)
    #M or F
    gender = models.CharField(max_length=1)
    #性取向
    seeking_gender = models.CharField(max_length=1)

    self_introduction = models.CharField(max_length=200)

    partner_expectation = models.CharField(max_length=200)

    image_url = models.CharField(max_length=200, default='')

    location_longitude = models.DecimalField(max_digits=9,decimal_places=6)
    location_latitude = models.DecimalField(max_digits=9,decimal_places=6)
    location_bucket = models.PositiveIntegerField()