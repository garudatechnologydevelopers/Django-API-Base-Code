
''' AUTHOR : GARUDA TECHNOLOGY '''

from rest_framework.serializers import ModelSerializer
from .models import *

class CarouselModelSerializer(ModelSerializer):
    class Meta:
        model = WebCarousel
        fields = '__all__'