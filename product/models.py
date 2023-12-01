from django.db import models
import uuid
from django_extensions.db.models import TimeStampedModel
from django.utils.text import slugify

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category/images/',null=True,blank=True)
    
    def __str__(self):
        return self.category_name
class ProductTypeModel(TimeStampedModel):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True,blank=True)
    product_type = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_type/images/',null=True,blank=True)

    def __str__(self):
        return self.product_type

class GoldProductModel(TimeStampedModel):
    PRODUCT_TYPE = (
        ("ring","Ring"),
        ("chain","Chain"),
        ("zumka","Zumka"),
        ("bangals","Bangals"),
        ("gantan","Gantan"),
        ("nath","Nath"),
    )

    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True,blank=True)
    product_type = models.ForeignKey(ProductTypeModel,on_delete=models.SET_NULL,null=True,blank=True)
    product_id = models.CharField(max_length=100,null=True,blank=True)
    product_name = models.CharField(max_length=100,null=True,blank=True)
    hu_id = models.CharField(max_length=20,null=True,blank=True)
    
    model = models.CharField(max_length=100,null=True,blank=True)
    sub_model = models.CharField(max_length=100,null=True,blank=True)
    gross_wt = models.CharField(max_length=255,blank=True,null=True)
    stone_wt = models.CharField(max_length=255,blank=True,null=True)
    purity_spec = models.CharField(max_length=255,blank=True,null=True)
    price = models.CharField(max_length=255,blank=True,null=True)
    description = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to='gold/images/',null=True,blank=True)
    quantity = models.IntegerField(blank=True,null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product_id}"

class ProductImages(models.Model):
    product = models.ForeignKey(GoldProductModel,on_delete=models.CASCADE,related_name='product_images')
    images = models.ImageField(upload_to='product/images')

    def __str__(self):
        return f"{self.product}"

