from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    email = models.EmailField(blank=False)
    picture = models.URLField(blank=False)
    
    def __str__(self):
        return self.user.username

class Experience(models.Model):
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} at {self.company}"

class Education(models.Model):
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100)
    school = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.degree} in {self.field_of_study} from {self.school}"
