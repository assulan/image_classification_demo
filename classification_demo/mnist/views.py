from rest_framework.views import APIView
from mnist.models import Image
from django.http import HttpResponse
import json
from rest_framework.parsers import MultiPartParser
from trained_models.code import predict
import os

class ImageView(APIView):
    """
    Image to classify.
    """
    parser_classes = (MultiPartParser, )

    def post(self, request):
        instance = Image(img=request.FILES['img'])
        instance.save()
        # predict class of the hand written digit
        # klass = predict.predict(instance.img.path, predict.LOG_REG)
        klass = predict.predict(instance.img.path, predict.CONV_MLP)

        # remove the image file and model instance
        # os.remove(instance.img.path)
        instance.delete()
        return HttpResponse(json.dumps({'imgClass': klass}))
