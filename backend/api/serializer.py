from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField
from app.models import Book, CartItem, CustomUser, Order



class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    
class CartitemSerializer(ModelSerializer):

    book = BookSerializer()
    total_amount = SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = '__all__'
    
    def get_total_amount(self, obj):
        return obj.book.price * obj.quantity
    
class OrderItemSerializer(ModelSerializer):
    
    total_amount = SerializerMethodField()
    book = BookSerializer()
    class Meta:
        model = Order
        fields = '__all__'

    def get_total_amount(self, obj):
        return obj.book.price * obj.quantity if obj.book else 0

        
class CustomUserSerializer(ModelSerializer):

    password = CharField(write_only=True)  
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'name', 'phone', 'address', 'college', 'username',   )

    def create(self, validated_data):
        user = CustomUser(**validated_data)
        password = self.validated_data['password']
        user.set_password(password)  
        user.save()
        return user
    
