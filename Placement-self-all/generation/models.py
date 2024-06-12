from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Details(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    email = models.EmailField(blank=False)
    picture = models.URLField(blank=False)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=30)
    address = models.CharField(max_length=100, blank=False)
    title = models.CharField(max_length=100, blank=True)
    techstack = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    degree = models.CharField(max_length=100, blank=True)
    field_of_study = models.CharField(max_length=100, blank=True)
    school = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
