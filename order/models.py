from django.db import models

# Create your models here.
from customer.models import Customer, Address
from product.models import Product
from django.utils.translation import gettext_lazy as _



class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_('quantity'),default=1)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    ordered = models.BooleanField(_('order status'),default=False)

    @property
    def product_price(self):
        return self.quantity * self.product.discount_price

    def __str__(self):
        return f'{self.product.name} -- quantity : {self.quantity} -- price:{self.product_price}'





class OrderHistory(models.Model):
    total_price = models.PositiveIntegerField(_('total price'),default=0)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='order_history')
    orders = models.ManyToManyField(Order, related_name='order_history')
    ordered_date = models.DateTimeField(_('order date'),auto_now_add=True)
    ordered = models.BooleanField(_('order status'),default=False)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    READY_TO_SEND = _('Ready to send')
    SENDING = _('Sending')
    DELIVERED = _('Delivered')
    send_status = (
        (READY_TO_SEND, READY_TO_SEND),
        (SENDING, SENDING),
        (DELIVERED, DELIVERED)
    )
    status = models.CharField(_('send status'),max_length=100,choices=send_status, default=READY_TO_SEND)

    class Meta:
        ordering = ['ordered_date']
        verbose_name = _('Order History')
        verbose_name_plural = _('Order Histories')



    def __str__(self):
        return f'customer:{self.customer.first_name} {self.customer.last_name} -- order_count:{self.orders.count()} -- status:{self.status}'
