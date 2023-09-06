from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets, permissions
from app.models import Book, CartItem, Order
from .serializer import BookSerializer, CartitemSerializer, CustomUserSerializer, OrderItemSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class CartItemViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    
    @action(detail=False, methods=['get'])
    def get_cart_items(self, request):
        user = request.user
        cart_items = CartItem.objects.filter(user=user)
        serializer = CartitemSerializer(cart_items, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def add_to_cart(self, request):
        user = request.user
        book_id = request.data.get('book_id')
        quantity = request.data.get('quantity')
        book = Book.objects.get(id=book_id)
        cart_item, created = CartItem.objects.get_or_create(user=user, book=book)
        cart_item.quantity += quantity
        cart_item.save()
        serializer = CartitemSerializer(cart_item)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def update_cart(self, request):
        user = request.user
        book_id = request.data.get('book_id')
        quantity = request.data.get('quantity')
        book = Book.objects.get(id=book_id)
        cart_item = CartItem.objects.get(user=user, book=book)
        serializer = CartitemSerializer(cart_item, data={'quantity': quantity}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    @action(detail=False, methods=['delete'])
    def delete_cart_item(self, request):
        user = request.user
        book_id = request.data.get('book_id')
        try:
            cart_item = CartItem.objects.get(user=user, book_id=book_id)
            cart_item.delete()
            return Response({'message': 'Cart item deleted successfully'})
        except CartItem.DoesNotExist:
            return Response({'message': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)

class OrderViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        user = request.user
        cart_items = CartItem.objects.filter(user=user)

        # if not cart_items:
        #     return Response({'message': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

        for cart_item in cart_items:
            existing_order = Order.objects.filter(user=user, book=cart_item.book).first()
            if existing_order:
                existing_order.quantity += cart_item.quantity
                existing_order.save()
            else:
                order = Order.objects.create(
                    user=user,
                    book=cart_item.book,
                    quantity=cart_item.quantity,
                )
            cart_item.delete()

        return Response({'message': 'Order placed successfully.'}, status=status.HTTP_201_CREATED)

class OrderItemViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class UserViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)

class SignUpViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    
