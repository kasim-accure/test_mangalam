from django.contrib import admin
from product.models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(ProductTypeModel)
admin.site.register(GoldProductModel)
admin.site.register(ProductImages)