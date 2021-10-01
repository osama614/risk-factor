from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
#from django.contrib.auth import get_user_model

#User = get_user_model()

# Create your models here
def upload_avater(instance, filename):
    extision = filename.split('.')[1]
    return 'users/avaters/%s.%s'%(instance.username,extision)

class User(AbstractUser):
      
    GENDER_CHOICES = (('male', "Male"),
              ("female", "Female"))
    avater = models.ImageField(blank=True, upload_to=upload_avater, null=True)
    country = models.CharField(max_length=30, blank=True)
    phone_number = PhoneNumberField(blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=100, blank=True)
    verified_email = models.BooleanField(default=False)
    verified_phone = models.BooleanField(default=False)
    age = models.IntegerField(blank=True, null=True)
  



class ChronicDisease (models.Model):
    owner = models.OneToOneField(User, related_name='chronic_disease',blank=True,null=True, on_delete=models.CASCADE)
    organ_transplant = models.BooleanField(default=False)
    pregnancy = models.BooleanField(default=False)
    cardiovascular_disease = models.BooleanField(default=False)
    COPD = models.BooleanField(default=False)
    renal_disease = models.BooleanField(default=False)
    cancer = models.BooleanField(default=False)
    hypertension = models.BooleanField(default=False)
    diabetes = models.BooleanField(default=False)
    

    class Meta:
        verbose_name = _('ChronicDisease')
        verbose_name_plural = _('ChronicDiseases')


    def __str__(self):
       return f" {self.owner.username}'s' ChronicDiseases List"