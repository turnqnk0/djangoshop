from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AbstractUser, AnonymousUser
from django.db.models import ManyToManyField
from django.forms.models import model_to_dict


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    zipcode = models.CharField(max_length=20, blank=True, verbose_name="zipcode")
    phone = models.CharField(max_length=100, blank=True, verbose_name="phone")
    date_of_birth = models.DateField(blank=False, null=True, verbose_name="birthdate")

    def __str__(self):
        return str(self.user.username)

    def get_user_profile(self):
        userprofile = model_to_dict(self,
                                    fields=[field.name for field in UserProfile._meta.fields],
                                    exclude=['user'])
        return dict(userprofile)


class Address(models.Model):
    street = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    userprofile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return str(self.userprofile)

