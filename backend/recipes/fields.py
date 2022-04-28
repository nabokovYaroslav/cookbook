from rest_framework.fields import ImageField as BaseImageField
from rest_framework.serializers import Serializer

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