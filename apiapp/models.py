
''' AUTHOR : GARUDA TECHNOLOGY '''

from django.db import models


class WebCarousel(models.Model):
    uid = models.CharField(max_length=100, unique=True , primary_key=True)
    title = models.CharField(max_length=10000) 
    image = models.ImageField(upload_to='webcarousel/')

    def __str__(self):
        return self.title

