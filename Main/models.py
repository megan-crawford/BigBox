from django.db import models
from django.contrib.gis.db import geoModel

# Create your models here.
class WorldBorder(geoModel.Model):
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    name = geoModel.CharField(max_length=50)
    area = geoModel.IntegerField()
    pop2005 = geoModel.IntegerField('Population 2005')
    fips = geoModel.CharField('FIPS Code', max_length=2)
    iso2 = geoModel.CharField('2 Digit ISO', max_length=2)
    iso3 = geoModel.CharField('3 Digit ISO', max_length=3)
    un = geoModel.IntegerField('United Nations Code')
    region = geoModel.IntegerField('Region Code')
    subregion = geoModel.IntegerField('Sub-Region Code')
    lon = geoModel.FloatField()
    lat = geoModel.FloatField()

    # GeoDjango-specific: a geometry field (MultiPolygonField)
    mpoly = geoModel.MultiPolygonField()

    # Returns the string representation of the model.
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'geodjango'