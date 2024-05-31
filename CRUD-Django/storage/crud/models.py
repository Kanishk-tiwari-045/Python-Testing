from django.db import models

# Create your models here.
class Location(models.Model):
    locationname = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.locationname
    

class Item(models.Model):
    itemname = models.CharField(max_length=100)
    date_added = models.DateField(auto_now_add=True)
    itemlocation = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.itemname