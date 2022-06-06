from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework.exceptions import AuthenticationFailed, ValidationError, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import update_last_login
from rest_framework.status import HTTP_201_CREATED
from rest_framework.decorators import action
from .models import Order, Product, Provider, User
from .serializers import OrderSerializer, ProductSerializer, ProviderSerializer, UserSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'user']


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProviderViewSet(ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class NotManyProductsViewSet(ModelViewSet):
    queryset = Product.objects.filter(Q(count__gt=0) & Q(count__lt=10))
    serializer_class = ProductSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['POST'], detail=False)
    def signup(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create(
            email=serializer.validated_data['email'],
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name'],
            )
        user.set_password(serializer.validated_data['password'])
        user.is_active = True
        user.save()

        return Response({'message': 'success'}, status=HTTP_201_CREATED)

    @action(methods=['POST'], detail=False)
    def login(self, request):
        if 'email' not in request.data:
            raise ValidationError({'email': 'Email must be provided'})
        if 'password' not in request.data:
            raise ValidationError({'password': ['Password must be provided']})

        if User.objects.filter(email=request.data.get('email')).exists():
            user = User.objects.filter(email=request.data.get('email'))
        else:
            raise NotFound({'message': 'User with provided credentials does not exist'})

        refresh = RefreshToken.for_user(user)
        response = Response()
        response.set_cookie('refresh', str(refresh))
        response.data = {'access': str(refresh.access_token)}
        return response

    @action(methods=['GET'], detail=False,
            permission_classes=[IsAuthenticated])
    def user(self, request):
        user = request.user
        data = UserSerializer(user).data
        return Response(data)

    @action(detail=True, methods=['POST'], url_path='set_password')
    def set_password(self, request, pk=None):
        if 'new_password' not in request.data:
            raise ValidationError({'password': 'Password must be provided'})

        password = request.data['new_password']
        user = self.get_object()
        user.set_password(password)
        user.save()
        return Response({'status': 'password set'})
