# views.py

from rest_framework import viewsets
from .models import Product , ProductImage
from .serializers import ProductSerializer, ProductImageSerializer
from rest_framework.parsers import MultiPartParser, FormParser

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser, FormParser]
    
    # def get_serializer_class(self, ):
    #     if self.request.method == 'GET':
    #         return ProductSerializer
    #     else:
    #         return ProductCreateSerializer 
    
    
class ProductImageViewSet(viewsets.ModelViewSet):

    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

    parser_classes = [MultiPartParser, FormParser]