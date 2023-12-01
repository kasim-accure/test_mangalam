from django.db import models
from users.models import User
from product.models import GoldProductModel
from django.db.models.signals import post_save,pre_save,post_delete
from django.dispatch import receiver
from django.db.models import Sum
from django_extensions.db.models import TimeStampedModel
from django.utils import timezone



class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    total_price = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user}"
    
class CartItems(models.Model):

    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True,blank=True,related_name='cart_cartitem')
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='user_cartitem')
    product = models.ForeignKey(GoldProductModel,on_delete=models.CASCADE,null=True,blank=True,related_name='product_cartitem')
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user}"


class Order(models.Model):

    STATUS_CHOICE = (
        ("pending","Pending"),
        ("approved","Approved"),
        ("delivered","Delivered"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(GoldProductModel, through='OrderItem')
    order_date = models.DateTimeField(default=timezone.now)
    total_price = models.FloatField(default=0)
    status = models.CharField(max_length=50, choices=STATUS_CHOICE,default='Pending')

    def __str__(self):
        return f'{self.user}'


class OrderItem(TimeStampedModel):
    STATUS_CHOICE = (
        ("pending","Pending"),
        ("approved","Approved"),
        ("delivered","Delivered"),
        ("decline","Decline"),
        ("cancelled","Cancelled"),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(GoldProductModel, on_delete=models.CASCADE,null=True,blank=True)
    price = models.FloatField(default=0,null=True,blank=True)
    quantity = models.IntegerField(default=1,null=True,blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICE,default='Pending',null=True,blank=True)

    def __str__(self):
        return f'{self.product}'
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(GoldProductModel, on_delete=models.CASCADE) 


@receiver(pre_save, sender=CartItems)
def correct_cartprice(sender, **kwargs):
    cart_items = kwargs["instance"]
    price_of_product = GoldProductModel.objects.get(id=cart_items.product.id)
    cart_items.price = cart_items.quantity * float(price_of_product.price)

    cart = Cart.objects.get(id=cart_items.cart.id)
    # cart = cart_items.cart
    # total_price = sum(item.price for item in cart.cart_cartitem.all())
    cart.total_price += cart_items.price
    cart.save()


# @receiver(post_delete, sender=CartItems)
# def update_cart_total_price(sender, instance, **kwargs):
#     cart = instance.cart
#     price_difference = instance.price
#     cart.total_price -= price_difference
#     cart.save()

@receiver(post_save, sender=CartItems)
def update_cart_total_price(sender, instance, created, **kwargs):
    cart = instance.cart
    items_prices_sum = cart.cart_cartitem.aggregate(total_price=Sum('price'))['total_price'] or 0
    cart.total_price = items_prices_sum
    cart.save()

@receiver(post_delete, sender=CartItems)
def update_cart_total_price_on_delete(sender, instance, **kwargs):
    cart = instance.cart
    items_prices_sum = cart.cart_cartitem.aggregate(total_price=Sum('price'))['total_price'] or 0
    cart.total_price = items_prices_sum
    cart.save()
