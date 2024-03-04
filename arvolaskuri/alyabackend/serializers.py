from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from .models import Instruction, DBPicture

#Serializer for database pictures
class DBPictureSerializer(serializers.Serializer):
   class Meta:
       model = DBPicture
       fields = ["id", "dbpicture_title","dbpicture"]


#Serializer for Instructions in database
class InstructionSerializer(serializers.Serializer):
    class Meta:
       model = Instruction
       fields = ["id", "instuction_title","instruction_text"]


#Serializer for Pictures received from frontend
class PictureSerializer(serializers.Serializer):
    picture = Base64ImageField(max_length=None, allow_empty_file=False)