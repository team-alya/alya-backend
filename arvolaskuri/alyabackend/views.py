from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render
from alyabackend.serializers import PictureSerializer
from rest_framework.views import APIView
from .prediction import label_detection
from PIL import Image 
import PIL 
import io

def test(request):
    return render(request, "test.html")


# Example usage in the Frontpage APIView
class Frontpage(APIView):
    def get(self, request, *args, **kwargs):
        # Replace the image_path with the actual path to the image file
        image_path = 'C:\\Users\\arina\\Alya\\tuoli.jpg'

        # Read the content of the image file
        with open(image_path, 'rb') as file:
            image_content = file.read()

        # Pass the content to label_detection function
        result = label_detection(io.BytesIO(image_content))
        
        return JsonResponse(result)


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

