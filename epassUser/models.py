from django.db import models
# from django.contrib.auth.models import AbstractUser
# from .manager import UserManager


class UserDetails(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    phone_number = models.IntegerField(null=True)
    mode_of_transport = models.CharField(max_length=30, null=True)
    age = models.IntegerField(null=True)
    no_of_persons = models.IntegerField(null=True)
    from_address = models.CharField(max_length=1000, null=True)
    to_address = models.CharField(max_length=1000, null=True)
    from_city = models.CharField(max_length=20, null=True)
    to_city = models.CharField(max_length=20, null=True)
    from_state = models.CharField(max_length=20, null=True)
    to_state = models.CharField(max_length=20, null=True)
    from_zip = models.IntegerField(null=True)
    to_zip = models.IntegerField(null=True)
    reason = models.CharField(max_length=2000, null=True)
    covid_status = models.CharField(max_length=3, null=True)
    aadhar_img = models.ImageField(upload_to='images/', null=True)
    submitted_date = models.DateTimeField(null=True)
    approved_date = models.DateTimeField(null=True)
    approval_status = models.CharField(max_length=20, null=True)
    reject_reason = models.CharField(max_length=2000, null=True, default='')
    from_count = models.IntegerField(default=0)
    to_count = models.IntegerField(default=0)


# class User(AbstractUser):
#     phone_number = models.CharField(max_length=12, unique=True)
#     is_phone_verified = models.BooleanField(default=False)
#     otp = models.CharField(max_length=6)
#
#     USERNAME_FIELD = 'phone_number'
#     REQUIRED_FIELDS = []
#     objects = UserManager()
