from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from base.models import Product, Order, OrderItem, ShippingAddress
from base.serializers import ProductSerializer, OrderItemSerializer, OrderSerializer
from datetime import datetime


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_order_items(request):
    user = request.user
    data = request.data
    order_items = data.get('orderItems')

    if order_items and len(order_items) == 0:
        return Response({'detail' : 'No order items'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        order = Order.objects.create(
            user=user,
            payment_method=data['paymentMethod'],
            tax_price=data['taxPrice'],
            shipping_price=data['shippingPrice'],
            total_price=data['totalPrice']
        )
        order.save()

        shipping_address = ShippingAddress.objects.create(
            order=order,
            address=data['shippingAddress']['address'],
            city=data['shippingAddress']['city'],
            postal_code=data['shippingAddress']['city'],
            country=data['shippingAddress']['country'],
            shipping_price=data['shippingPrice']
        )
        shipping_address.save()

        for item in order_items:
            product = Product.objects.get(_id=item['product'])
            item = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                quantity=item['quantity'],
                price=item['price'],
                image=product.image.url
            )
            product.count_in_stock -= item.quantity
            product.save()

        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_orders(request):
    user = request.user
    orders = user.order_set.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_by_id(request, pk):
    user = request.user
    try:
        order = Order.objects.get(_id=pk)
    except Order.DoesNotExist:
        return Response({'detail': 'Order does not exist'},
                        status=status.HTTP_400_BAD_REQUEST)
    if user.is_staff or order.user == user:
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)
    else:
        return Response({'detail': 'Not authorized to view this order'},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_order_to_paid(request, pk):
    try:
        order = Order.objects.get(_id=pk)
    except Order.DoesNotExist:
        return Response({'detail': 'Order does not exist'},
                        status=status.HTTP_400_BAD_REQUEST)

    order.is_paid = True
    order.paid_at = datetime.now()
    order.save()

    return Response({'detail': 'Order was paid'})


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_orders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_order_to_delivered(request, pk):
    order = Order.objects.get(_id=pk)
    order.is_delivered = True
    order.delivered_at = datetime.now()
    order.save()
    return Response('Order was delivered')