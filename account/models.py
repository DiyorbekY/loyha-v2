from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

phone_relax = RegexValidator(
    regex=r'^\+998\d{9}$',
    message="Raqam shu formatda bo'lishi kerak: '+998xxxxxxxxx'."
)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(validators=[phone_relax], max_length=13, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    profil_image = models.ImageField(upload_to='profiles/', null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
