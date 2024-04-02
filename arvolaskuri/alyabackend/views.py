from io import BytesIO
from django.shortcuts import render
from django.http import JsonResponse
from alyabackend.serializers import  PictureSerializer
from rest_framework.views import APIView
from .prediction import label_detection
from PIL import Image 
from alyabackend.models import Instruction
from alyabackend.models import DBPicture
import io
from alyabackend.allas_bucket import *



# Instructions from backend
class InstructionsJson(APIView):
    def get(self, request, *args, **kwargs):

        # Fetch instruction data
        instructions = Instruction.objects.all().values()
        instructions_list = list(instructions)
        
        # Fetch picture data
        pictures = DBPicture.objects.all()
        picture_data = [{'title': picture.dbpicture_title, 'image_url': picture.dbpicture.url} for picture in pictures]
        
        # Combine instructions and picture data
        response_data = {
            'instructions': instructions_list,
            'pictures': picture_data
        }
        
        return JsonResponse(response_data, safe=False)

#Handling pictures send to backend
class ReceivePic(APIView):
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            furnitureDict = {
                "brand": request.data["brand"],
                "material": request.data["material"],
                "condition":request.data["condition"],
                "model": request.data["model"],
                "priceWhenNew": request.data["priceWhenNew"],
                "age": request.data["age"]
            }
            #Creating serializer instance
            serializer = PictureSerializer(data=request.data)
            if serializer.is_valid():
                picture = serializer.validated_data["picture"]
                result = label_detection(picture,furnitureDict)
                message = result
                #store_image(picture, request.data["brand"], request.data["model"])
            else:
                uploaded_file = request.FILES.get('picture')
                result = label_detection(uploaded_file)
                message = result
                #store_image(picture, request.data["brand"], request.data["model"])
        return JsonResponse({"message" : message})
    


