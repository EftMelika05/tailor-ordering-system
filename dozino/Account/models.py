from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
 #delete role
  full_name=models.CharField(max_length=100)

  phone_number=models.CharField(max_length=11 , unique=True,
                                validators=[RegexValidator(r'^09\d{9}$',
  'شماره موبایل معتبر نیست')])

  address=models.TextField(blank=True)

  postal_code=models.CharField(max_length=10,blank=True)

  gender_choice=[('woman' , 'زن') , ('man' , 'مرد')]
  gender=models.CharField(max_length=20 , choices=gender_choice)



  '''
  role_choices=[('customer','مشتری'),('tailor','خیاط')]
  role=models.CharField(max_length=20 , choices=role_choices)

  '''
    
  def __str__(self):
    return self.username