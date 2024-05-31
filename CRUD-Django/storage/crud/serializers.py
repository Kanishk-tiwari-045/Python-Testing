from rest_framework import serializers
from .models import *

class ItemSerializers(serializers.ModelSerializer):
    itemname = models.CharField(max_length=100)
    date_added = models.DateField(auto_now_add=True)
    itemlocation = models.ForeignKey(Location, on_delete=models.CASCADE)
    class Meta:
        model = Item
        fields = ('__all__')

class LocationSerializers(serializers.ModelSerializer):
    locationname = models.CharField(max_length=100, unique=True)
    class Meta:
        model = Location
        fields = ('__all__')