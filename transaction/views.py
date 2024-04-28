from rest_framework import decorators, request
from rest_framework.response import Response
from rest_framework import status

from django.db import transaction, DatabaseError
from django.db.models import F

from functools import partial

from .serializer import OrderSerialzer
from .models import Order, Product



def default_behavior(req: request.Request):
    serializer = OrderSerialzer(data=req.data)
    serializer.is_valid()

    product_id, num_of_items = serializer.data["product"], serializer.data["number_of_items"]
    product = Product.objects.get(id=product_id)

    return product, num_of_items


def email_user(email="default@email.com"):
    print(f"Email sent to {email} successfully")


@decorators.api_view(["POST"])
def success_atomic(req: request.Request):
    product, num_of_items = default_behavior(req)
    
    with transaction.atomic():
        product.number_in_stock = F("number_in_stock") - num_of_items
        product.save()

        Order.objects.create(product=product, number_of_items=num_of_items)

    return Response({"message": "transaction done"},
        status=status.HTTP_201_CREATED)


@decorators.api_view(["POST"])
def un_success_atomic(req: request.Request):
    product, num_of_items = default_behavior(req)
    
    with transaction.atomic():
        product.number_in_stock = F("number_in_stock") - num_of_items
        product.save()

        # server crash simulation
        import sys
        sys.exit(1)

        Order.objects.create(product=product, number_of_items=num_of_items)

    return Response({"message": "transaction done"},
        status=status.HTTP_201_CREATED)


@decorators.api_view(["POST"])
def atomic_commit_no_param(req: request.Request):
    product, num_of_items = default_behavior(req)
    
    with transaction.atomic():
        product.number_in_stock = F("number_in_stock") - num_of_items
        product.save()

        Order.objects.create(product=product, number_of_items=num_of_items)

    transaction.on_commit(email_user)

    return Response({"message": "transaction done"},
        status=status.HTTP_201_CREATED)


@decorators.api_view(["POST"])
def atomic_commit_with_param(req: request.Request):
    product, num_of_items = default_behavior(req)
    
    with transaction.atomic():
        product.number_in_stock = F("number_in_stock") - num_of_items
        product.save()

        Order.objects.create(product=product, number_of_items=num_of_items)

    transaction.on_commit(partial(email_user, email="maamoun.haj.najeeb@gmail.com"))

    return Response({"message": "transaction done"},
        status=status.HTTP_201_CREATED)


@decorators.api_view(["POST"])
def atomic_handled_error(req: request.Request):
    product, num_of_items = default_behavior(req)
    
    try:
        with transaction.atomic():

            product.number_in_stock = F("number_in_stock") - num_of_items
            product.save()

            Order.objects.create(product=product)

    except DatabaseError:
        Order.objects.create(product=product, number_of_items=num_of_items)

    transaction.on_commit(partial(email_user, email="maamoun.haj.najeeb@gmail.com"))

    return Response({"message": "transaction done"},
        status=status.HTTP_201_CREATED)
