from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render
from alyabackend.serializers import PictureSerializer
from rest_framework.views import APIView


def test(request):
    return render(request, "test.html")


#Sending info to frontpage
class Frontpage(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"info": "Here is some info about taking pictures", "picture": "here could be picture"})



#Handling pictures send to backend
class ReceivePic(APIView):
    message = ""
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            #Creating serializer instance
            serializer = PictureSerializer(data=request.data)
            if serializer.is_valid():
                picture = serializer.validated_data["picture"]
                message = "I have received your picture, thanks"
            else:
                message = "I have you know that this endpoint only accepts Base64 pictures"
        return JsonResponse({"message" : message})
