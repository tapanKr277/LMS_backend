from . import views
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'books', views.BookViewSet, basename='books')
router.register(r'cartitems', views.CartItemViewSet, basename='cartitems')
router.register(r'orders', views.OrderViewSet, basename='orders')
router.register(r'orderitems', views.OrderItemViewSet, basename='orderitems')
router.register(r'user', views.UserViewSet, basename='user')
router.register(r'signup', views.SignUpViewSet, basename='signup')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  
]