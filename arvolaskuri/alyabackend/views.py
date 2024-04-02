from io import BytesIO
from django.shortcuts import render
from django.http import JsonResponse
from alyabackend.serializers import  PictureSerializer
from rest_framework.views import APIView
from .prediction import label_detection
from PIL import Image 
from alyabackend.models import Instruction
import io
from alyabackend.allas_bucket import *



# Example usage in the Frontpage APIView
class Frontpage(APIView):
    def get(self, request, *args, **kwargs):
        #Getting instructions from database
        response = Instruction.objects.values("instruction_text").get(pk=0)
        return JsonResponse({"response":response})


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
    


