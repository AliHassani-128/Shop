from django.db import models

# Create your models here.
from customer.models import Customer
from product.models import Product


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


    @property
    def product_price(self):
        return self.quantity * self.product.price


class OrderHistory(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    products = models.ManyToManyField(Order)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    READY_TO_SEND = 1
    SENDING = 2
    DELIVERED = 3
    send_status = (
        (READY_TO_SEND, 'آماده ارسال'),
        (SENDING, 'در حال ارسال'),
        (DELIVERED, 'تحویل شده')
    )
    status = models.PositiveIntegerField(choices=send_status,default=READY_TO_SEND)

    class Meta:
        ordering = ['ordered_date']

    @property
    def total_price(self):
        total = 0
        for order in self.products.all():
            total += order.product_price
        return total

    @property
    def set_discount(self, discount):
        return (self.total_price * discount) / 100


from django.core.validators import MinValueValidator, MaxValueValidator


class DiscountCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField()

    def __str__(self):
        return self.code
