from base.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from base.serializers import UserSerializer, JWTTokenObtainPairSerializer, UserSerializerWithToken
from django.contrib.auth.hashers import make_password


class JWTTokenObtainPairView(TokenObtainPairView):
    serializer_class = JWTTokenObtainPairSerializer


@api_view(['POST'])
def register_user(request):
    data = request.data

    try:
        user = User.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except Exception as ex:
        message = {'detail': str(ex)}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    user = request.user
    serializer = UserSerializerWithToken(user, many=False)

    data = request.data
    user.first_name = data['name']
    user.username = user.email = data['email']

    if data['password'] != '':
        user.password = make_password(data['password'])

    user.save()

    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_user(request, pk):
    user = User.objects.get(id=pk)
    user.delete()
    return Response({'detail': 'User was deleted'})


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_user_by_id(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request, pk):
    user = User.objects.get(id=pk)

    data = request.data
    user.first_name = data['name']
    user.username = user.email = data['email']
    user.is_staff = data['is_admin']

    user.save()

    serializer = UserSerializer(user, many=False)

    return Response(serializer.data)