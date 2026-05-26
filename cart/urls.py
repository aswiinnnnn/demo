from django.urls import path
from .views import cart_list_create, cart_detail


urlpatterns = [
    path("cart/", cart_list_create, name="cart-list-create"),
    path("cart/<int:pk>/", cart_detail, name="cart-detail"),
]
