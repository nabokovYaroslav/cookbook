from rest_framework.fields import ImageField as BaseImageField
from rest_framework.serializers import Serializer
from drf_extra_fields.fields import Base64ImageField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from utils.image import get_adaptive_image, get_tumbnail
from utils.srcset import get_srcset


class ImageField(BaseImageField):
    def to_representation(self, value):
        url = super().to_representation(value)
        extension_image = self.context.get("extension_image", None)

        image_object = {}
        image_object["url"] = get_adaptive_image(url, extension_image)
        image_object["srcset"] = get_srcset(url, extension_image)
        
        return image_object

class TumbnailImageField(BaseImageField):
    def to_representation(self, value):
        url = super().to_representation(value)
        extension_image = self.context.get("extension_image", None)
        url = get_tumbnail(url, extension_image)
        
        return url

class RecursiveField(Serializer):
    def to_representation(self, value):
        # self.parent.parent.__class__ equal serailizer where this field declared
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class CustomBase64ImageField(Base64ImageField):
    def to_internal_value(self, base64_data):
        if base64_data in self.EMPTY_VALUES:
            raise ValidationError(_("Invalid type. This is not an base64 string: {}".format(type(base64_data))))
        return super().to_internal_value(base64_data)