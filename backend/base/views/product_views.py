from base.models import Product
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from base.serializers import ProductSerializer
from rest_framework import status

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


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_product(request, pk):
    product = Product.objects.get(_id=pk)
    product.delete()
    return Response({'detail': 'Product deleted'})


@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_product(request):
    user = request.user
    product = Product.objects.create(
        user=user,
        name='Sample Name',
        price=0,
        brand='Sample Brand',
        count_in_stock=0,
        category='Sample Category',
        description=''
    )
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_product(request, pk):
    try:
        product = Product.objects.get(_id=pk)
    except Product.DoesNotExist:
        return Response({'detail': 'Product does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        data = request.data

        try:
            product.name = data['name']
            product.price = data['price']
            product.brand = data['brand']
            product.count_in_stock = data['count_in_stock']
            product.category = data['category']
            product.description = data['description']

            product.save()
            serializer = ProductSerializer(product, many=False)
            return Response(serializer.data)
        except KeyError:
            return Response({'detail': 'Request error'}, status=status.HTTP_400_BAD_REQUEST)