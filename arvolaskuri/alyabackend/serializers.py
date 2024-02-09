from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

class PictureSerializer(serializers.Serializer):
    picture = Base64ImageField(max_length=None, allow_empty_file=False)