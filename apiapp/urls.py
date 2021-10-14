
''' AUTHOR : GARUDA TECHNOLOGY '''

from django.urls import path
from .views import *

urlpatterns = [ 
    path('web-carousel-create/', WebServicesCreate.as_view(), name='web-carousel-create'),
    path('web-carousel-put/', WebServicemodify.as_view(), name='web-carousel-put'),
    path('login-admin-user/',AdminLogin.as_view()),

]