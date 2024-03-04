import io
from io import BytesIO
from django.shortcuts import render
from django.http import JsonResponse
from alyabackend.serializers import  PictureSerializer
from rest_framework.views import APIView
from .prediction import label_detection
from PIL import Image 
from alyabackend.models import Instruction
import io

def test(request):
    return render(request, "test.html")


# Example usage in the Frontpage APIView
class Frontpage(APIView):
    def get(self, request, *args, **kwargs):
        #Getting instructions from database
        response = Instruction.objects.values("instruction_text").get(pk=1)
        return JsonResponse(response)


#Handling pictures send to backend
class ReceivePic(APIView):
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            #Creating serializer instance
            serializer = PictureSerializer(data=request.data)
            if serializer.is_valid():
                picture = serializer.validated_data["picture"]

                result = label_detection(picture)
                message = result
                
            else:
                uploaded_file = request.FILES.get('picture')
                result = label_detection(uploaded_file)
                message = result
               # message = "I have you know that this endpoint only accepts Base64 pictures"
        return JsonResponse({"message" : message})

