from django.http import JsonResponse
from alyabackend.serializers import  PictureSerializer
from rest_framework.views import APIView
from .prediction import label_detection 
from alyabackend.models import Instruction
from alyabackend.allas_bucket import *
from alyabackend.models import DBPicture


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
            #Creating serializer instances. Pointing to an serializer consumes the image,
            #so we need two serializers.
            serializerForVertex = PictureSerializer(data=request.data)
            serializerForAllas = PictureSerializer(data=request.data)
            if serializerForVertex.is_valid()& serializerForAllas.is_valid():
            
                pictureForAllas = serializerForAllas.validated_data["picture"]
                pictureForVertex= serializerForVertex.validated_data["picture"]
                
                #This sends the picture to Allas and receives name of the image
                #This also consumes the serialized image, and it cannot be used further
                image_name = store_image(pictureForAllas)
                
                #This sends the image to Vertex and consumes the image.
                result = label_detection(pictureForVertex,furnitureDict)
                message = result
            else:
                uploaded_file = request.FILES.get('picture')
                result = label_detection(uploaded_file)
                message = result
                image_name = store_image(pictureForAllas)
        return JsonResponse({"message" : message})
    


