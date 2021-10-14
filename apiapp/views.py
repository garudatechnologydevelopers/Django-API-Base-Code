
''' AUTHOR : GARUDA TECHNOLOGY '''

from django.contrib.auth import authenticate
import uuid

from rest_framework.authtoken.models import Token
from apiapp.authentication import AdminAuthentication, SuperAdminPermission
from django.contrib.auth.models import User

# Authentication PermissionS
from .models import *
from apiapp.serializers import *

# RESTFRAMEWORK
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# RESPONSE IMPORT 
from apiview.responsecode import display_response , SUCCESS , exceptionmsg , exceptiontype

"web services create"
class WebServicesCreate(APIView):

    serializer_class =  CarouselModelSerializer
    authentication_classes = [AdminAuthentication]
    permission_classes = [SuperAdminPermission]

    def get(self , request , format = None):
        snippet = WebCarousel.objects.all()
        if snippet is None:
            return Response(status.HTTP_404_NOT_FOUND , 'No Carousel Found')
        serializer = CarouselModelSerializer(snippet , many = True , context ={'request' : request})
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    def post(self , request , format = None):
        title = request.POST.get('title')
        image = request.FILES.get('image')
        print("web carousel" , title , image)

        if image in [None,""] or title in [None ,""]:
            return display_response(status.HTTP_404_NOT_FOUND, 'Values found none' , "web carousel creating")

        while True:
            uid = uuid.uuid3(uuid.NAMESPACE_DNS , title)
            check_uid = WebCarousel.objects.filter(uid = uid).first()
            if check_uid is None:
                break 

        try:
            WebCarousel.objects.create(
                uid = uid , 
                title = title ,
                 image = image
                 )
            return display_response( 'Web Carousel Created' , "success"  , status.HTTP_201_CREATED )
        except Exception as e: 
            excep = exceptiontype(e)
            msg = exceptionmsg(e)
            return display_response("WeB Carousel Create",f"{excep} || {msg}",status.HTTP_409_CONFLICT)

'''WEB CAROUSEL MODIFY'''
class WebServicemodify(APIView):
    serializer_class =  CarouselModelSerializer
    authentication_classes = [AdminAuthentication]
    permission_classes = [SuperAdminPermission]

    def put(self, request ,format=None):
        data = request.data
        print("web carousel modify" , data)
        uid = request.GET.get('uid')
        title = request.GET.get('title')
        image = request.FILES.get('image')  #FILES parameter through POST parameter

        '''Check if value is None or not'''
        if uid in [None,""]:
            return display_response("Web Carousel Update","Web carousel values was found None",status.HTTP_404_NOT_FOUND)

        carousel = WebCarousel.objects.filter(uid=uid).first()
        if carousel is None:
            return display_response("Web Carousel update objects","WebCarousel object was not found",status.HTTP_404_NOT_FOUND)

        if title not in [None,""]:
            carousel.title = title
            carousel.save()
            return display_response("Title Updating","Title Object Updated",status.HTTP_200_OK)
        
        if image not in [None,""]:
            carousel.image = image
            carousel.save()
            return display_response("image Updating","image Object Updated",status.HTTP_200_OK)
        return display_response("Nothing Updating","no Object Updated",status.HTTP_200_OK)
        
    def delete(self , request , format = None):
        uid = request.GET.get('uid')
        if uid is  None:
            return display_response("Web Carousel Delete","Web carousel values was found None",status.HTTP_404_NOT_FOUND)
        carousel = WebCarousel.objects.filter(uid=uid).first()
        if carousel is None:
            return display_response("carousel delete" , "no objects found" , status.HTTP_404_NOT_FOUND)
        
        try:
            carousel.delete()
            return display_response("Web Carousel Delete" , "success" , status.HTTP_200_OK)
        except Exception as e:
            excep = exceptiontype(e)
            msg = exceptionmsg(e)
            return display_response("Web Carousel Delete",f"{excep} || {msg}",status.HTTP_409_CONFLICT)
"""ADMIN CREATING"""

class AdminLogin(APIView):
    authentication_classes=[]
    permission_classes=[]

    def post(self,request,format=None):
        data=self.request.data
        username=data['username']
        password=data['password']


        user=authenticate(username=username,password=password)
        print("user ================" , user)
        if user is not None:
            token=Token.objects.get_or_create(user=user)
            print("token ================" , token)
            if(user.is_superuser):
                return Response({"RESPONSE":{"token":token[0].key,"superuser":True , "superadmin" : username}},status=status.HTTP_200_OK)
            return Response({"RESPONSE":{"token":token[0].key}},status=status.HTTP_200_OK)


        return Response({"RESPONSE":"Invalid credentials given"},status=status.HTTP_400_BAD_REQUEST)
