from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
 
  role_choices=[('customer','مشتری'),('tailor','خیاط')]
  role=models.CharField(max_length=20 , choices=role_choices)
  full_name=models.CharField(max_length=100,blank=True)
  phone_number=models.CharField(max_length=11 , unique=True,
                                validators=[RegexValidator(r'^09\d{9}$',
            'شماره موبایل معتبر نیست')])
  address=models.CharField(blank=True, max_length=300)
  
  def __str__(self):
    return self.username