from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
 
  role_choices=[('customer','مشتری'),('tailor','خیاط')]
  role=models.CharField(max_length=20 , choices=role_choices)
  phone_number=models.CharField(max_length=11 , 
                                validators=[RegexValidator(r'^09\d{9}$',
            'شماره موبایل معتبر نیست')])
  address=models.TextField()
  postal_code=models.CharField(max_length=10)
  
  def __str__(self):
    return self.username