from django.contrib import admin
from carts.models import *


admin.site.register(Cart)
admin.site.register(CartItems)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Favorite)
