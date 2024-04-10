import io
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
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .prices import price_detection
import json

def test(request):
    return render(request, "test.html")


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
            #Creating serializer instance4
            
            furnitureDict = {
                "brand": request.data["brand"],
                "material": request.data["material"],
                "condition":request.data["condition"],
                "model": request.data["model"],
                "priceWhenNew": request.data["priceWhenNew"],
                "age": request.data["age"]
            }


            serializer = PictureSerializer(data=request.data)
            if serializer.is_valid():
                picture = serializer.validated_data["picture"]

                result = label_detection(picture,furnitureDict)
                message = result
                
            else:
                uploaded_file = request.FILES.get('picture')
                result = label_detection(uploaded_file)
                message = result
               # message = "I have you know that this endpoint only accepts Base64 pictures"
        return JsonResponse({"message" : message})
    
#Handling form data


class AskPrice(APIView):

    def post(self, request, *args, **kwargs):
        filled_form = {
            "brand": request.data.get("brand"),
            "material": request.data.get("material"),
            "condition": request.data.get("condition"),
            "model": request.data.get("model"),
            "priceWhenNew": request.data.get("priceWhenNew"),
            "age": request.data.get("age")
        }

        serializer = PictureSerializer(data=request.data)
        if serializer.is_valid():
            picture = serializer.validated_data["picture"]
            
            try:
                result = price_detection(picture, filled_form)
                return JsonResponse(result)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
        else:
            return JsonResponse({"error": "Picture serialization failed."}, status=400)