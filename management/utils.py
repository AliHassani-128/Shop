import logging

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


def set_staff_group():

    PERMISSIONS = ('delete','view','change','add')
    MODELS = ('Customer','Category','product','discountcode','order','Order History',)
    try:
        staff_group = Group.objects.get(name='staff_group')
    except Group.DoesNotExist:
        staff_group = Group.objects.create(name='staff_group')
        for model in MODELS:
            for perm in PERMISSIONS:
                if model == 'discountcode':
                    name = 'Can {} {}'.format(perm, 'discount code')
                else:
                    name = 'Can {} {}'.format(perm, model)
                try:
                    print(name)
                    if model == 'Order History':
                        model_add_perm = Permission.objects.get(name=name,content_type__model__icontains='order')

                    else:
                        try:
                            model_add_perm = Permission.objects.get(name=name,content_type__model__icontains=model)
                        except Permission.MultipleObjectsReturned:
                            model_add_perm = Permission.objects.filter(name=name,content_type__model__icontains=model).first()
                except Permission.DoesNotExist:
                    print("Permission not found with name '{}'.".format(name))
                    continue

                staff_group.permissions.add(model_add_perm)


    return staff_group