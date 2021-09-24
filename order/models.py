from django.db import models

# Create your models here.
from customer.models import Customer
from product.models import Product


from django.core.validators import MinValueValidator, MaxValueValidator


class DiscountCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField()

    def __str__(self):
        return self.code


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    @property
    def product_price(self):
        return self.quantity * self.product.discount_price

    def __str__(self):
        return f'{self.product.name} -- quantity : {self.quantity} -- price:{self.product_price}'


class OrderHistory(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT,related_name='order_history')
    orders = models.ManyToManyField(Order,related_name='order_history')
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    discount_code = models.ForeignKey(DiscountCode,on_delete=models.CASCADE,null=True,blank=True)
    READY_TO_SEND = 1
    SENDING = 2
    DELIVERED = 3
    send_status = (
        (READY_TO_SEND, 'Ready to send'),
        (SENDING, 'Sending'),
        (DELIVERED, 'Delivered')
    )
    status = models.PositiveIntegerField(choices=send_status,default=READY_TO_SEND)

    class Meta:
        ordering = ['ordered_date']
        verbose_name = 'Order History'
        verbose_name_plural = 'Order Histories'

    @property
    def total_price(self):
        total = 0
        for order in self.orders.all():
            total += order.product_price
        return total

    @property
    def set_discount(self):
        if self.discount_code:
            return self.total_price - (self.total_price * self.discount_code.discount) / 100

    def __str__(self):
        return f'customer:{self.customer.first_name} {self.customer.last_name} -- order_count:{self.orders.count()} -- status:{self.status}'

