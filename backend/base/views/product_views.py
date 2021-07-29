from base.models import Product
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.serializers import ProductSerializer


@api_view(['GET'])
def get_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_product(request, pk):
    try:
        product = Product.objects.get(_id=pk)
    except Product.DoesNotExist:
        return Response(None)
    else:
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)