from base.models import Product, Review
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from base.serializers import ProductSerializer
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@api_view(['GET'])
def get_products(request):
    query = request.query_params.get('keyword')
    if query is None:
        query = ''

    products = Product.objects.filter(name__icontains=query)

    page = request.query_params.get('page')
    paginator = Paginator(products, 2)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    if page is None:
        page = 1

    page = int(page)

    serializer = ProductSerializer(products, many=True)
    return Response({'products': serializer.data, 'page': page, 'pages': paginator.num_pages})


@api_view(['GET'])
def get_top_products(request):
    products = Product.objects.filter(rating__gte=4).order_by('-rating')[:5]
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


@api_view(['POST'])
def upload_image(request):
    data = request.data
    product_id = data['product_id']
    product = Product.objects.get(_id=product_id)

    if product:
        product.image = request.FILES.get('image')
        product.save()
    else:
        return Response({'detail': 'No such product'}, status=status.HTTP_400_BAD_REQUEST)

    return Response('Image was uploaded')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product_review(request, pk):
    user = request.user
    data = request.data
    product = Product.objects.get(_id=pk)

    if product.review_set.filter(user=user).exists():
        content = {'detail': 'Product already reviewed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif data.get('rating') is None or data.get('rating') == 0:
        content = {'detail': 'Please select a rating'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    else:
        review = Review.objects.create(
            user=user,
            product=product,
            name=user.first_name,
            rating=data['rating'],
            comment=data.get('comment')
        )
        review.save()
        reviews = product.review_set.all()
        product.num_reviews = len(reviews)
        product.rating = sum(product_review.rating for product_review in reviews) / len(reviews)
        product.save()
        return Response('Review Add')