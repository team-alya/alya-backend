from django.http import JsonResponse
from rest_framework.views import APIView

from alyabackend.serializers import PictureSerializer
from alyabackend.models import Instruction, DBPicture
from alyabackend.allas_bucket import *
from .prediction import label_detection
from .prices import price_detection
from .repair import repairing_instructions


# API View to return instructions and pictures
class InstructionsJson(APIView):
    def get(self, request, *args, **kwargs):
        # Get all instructions from the database
        instructions = Instruction.objects.all().values()
        # Convert instructions to a list
        instructions_list = list(instructions)

        # Get all pictures from the database
        pictures = DBPicture.objects.all()
        # Create a list of dictionaries with picture title and url
        picture_data = [
            {"title": picture.dbpicture_title, "image_url": picture.dbpicture.url}
            for picture in pictures
        ]

        # Prepare the response data
        response_data = {"instructions": instructions_list, "pictures": picture_data}

        # Return the response data as JSON
        return JsonResponse(response_data, safe=False)


# API View to receive a picture and return the result of label detection
class ReceivePic(APIView):
    def post(self, request, *args, **kwargs):
        # Creating serializer instances. Pointing to an serializer consumes the image,
        # so we need two serializers.
        serializer_for_vertex = PictureSerializer(data=request.data)
        serializer_for_allas = PictureSerializer(data=request.data)

        # If both serializers are valid
        if serializer_for_vertex.is_valid() and serializer_for_allas.is_valid():
            # Get the picture data
            picture_for_allas = serializer_for_allas.validated_data["picture"]
            picture_for_vertex = serializer_for_vertex.validated_data["picture"]

            # This sends the picture to Allas and receives name of the image
            # This also consumes the serialized image, and it cannot be used further
            # image_name = store_image(pictureForAllas)

            try:
                # Perform label detection on the picture
                result = label_detection(picture_for_vertex)
                # Return the result as JSON
                return JsonResponse(result)
            except Exception as e:
                # If an error occurs, return the error message as JSON
                return JsonResponse({"error": str(e)}, status=500)
        else:
            # If the serializers are not valid, return an error message
            return JsonResponse({"error": "Picture serialization failed."}, status=400)


# API View to receive a picture and furniture data and then return the result of price prediction
class AskPrice(APIView):
    def post(self, request, *args, **kwargs):
        # Get the filled form data from frontend
        filled_form = {
            "type": request.data.get("type"),
            "brand": request.data.get("brand"),
            "model": request.data.get("model"),
            "color": request.data.get("color"),
            "dimensions": request.data.get("dimensions"),
            "condition": request.data.get("condition"),
            "age": request.data.get("age"),
        }

        # Serialize the incoming picture data
        serializer = PictureSerializer(data=request.data)

        # If the serializer is valid
        if serializer.is_valid():
            # Get the picture data
            picture = serializer.validated_data["picture"]

            try:
                # Perform price detection on the picture and furniture data
                result = price_detection(picture, filled_form)
                # Return the result as JSON
                return JsonResponse(result)
            except Exception as e:
                # If an error occurs, return the error message as JSON
                return JsonResponse({"error": str(e)}, status=500)
        else:
            # If the serializer is not valid, return an error message
            return JsonResponse({"error": "Picture serialization failed."}, status=400)


class Repair(APIView):
    def post(self, request, *args, **kwargs):
        # Get the filled form data from frontend
        filled_form = {
            "type": request.data.get("type"),
            "brand": request.data.get("brand"),
            "model": request.data.get("model"),
            "color": request.data.get("color"),
            #"dimensions": request.data.get("dimensions"),
            "condition": request.data.get("condition"),
            #"material": request.data.get("material")
        }

        # Serialize the incoming picture data
        serializer = PictureSerializer(data=request.data)

        # If the serializer is valid
        if serializer.is_valid():
            # Get the picture data
            picture = serializer.validated_data["picture"]

            try:
                # Perform price detection on the picture and furniture data
                result = repairing_instructions(picture, filled_form)
                # Return the result as JSON
                return JsonResponse(result)
            except Exception as e:
                # If an error occurs, return the error message as JSON
                return JsonResponse({"error": str(e)}, status=500)
        else:
            # If the serializer is not valid, return an error message
            return JsonResponse({"error": "Picture serialization failed."}, status=400)
