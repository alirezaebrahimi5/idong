from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Cart, CartVote, Product
from groups.models import Group
from .serializers import *


class CartCreateView(APIView):
    """
    POST: create a cart for given group
    GET: Shows a Cart with given ID (Detail)
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        cart_id = request.query_params.get('cart_id')

        # check if there is cart_id
        if not cart_id:
            return Response({'message': 'please give am cart_id'}, status.HTTP_400_BAD_REQUEST)

        cart = get_object_or_404(Cart, id=cart_id)

        # check if user is in the group
        if self.request.user not in cart.group.members.all():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = CartDetailSerializer(cart)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        serializer = CartCreateSerializer(data=request.data)
        if serializer.is_valid():
            # group object
            group = serializer.validated_data["group"]

            # get all the groups member
            group_members = group.members.all()

            # check if user is exist in the group
            if self.request.user not in group_members:
                return Response(status=status.HTTP_404_NOT_FOUND)

            # check if all the given users are in the given group
            for user in serializer.validated_data["users"]:
                if user not in group_members:
                    return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

            users_to_add = serializer.validated_data["users"]
            users_to_add.append(self.request.user)

            # get the sum of the users that are going to join to Cart
            users_len = len(serializer.validated_data["users"])

            # create the Cart
            cart = Cart.objects.create(
                title=serializer.validated_data["title"],
                owner=self.request.user,
                group=group,
                users_sum=users_len,
                description=serializer.validated_data["description"],
                image=serializer.validated_data["image"],
            )
            cart.users.add(*users_to_add)
            cart.save()
            return Response(CartSerializer(cart).data, status.HTTP_200_OK)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class CartProductView(APIView):
    """
    POST: Creates a new Product and add it to given Cart
    PUT: Updates a product
    DELETE: Deletes a product
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = CartProductSerializer(data=request.data)
        if serializer.is_valid():
            cart = serializer.validated_data["cart"]

            # throw an error if user is not in cart users
            if self.request.user not in cart.users.all():
                return Response(status=status.HTTP_403_FORBIDDEN)

            # throw an error if user is not in group
            if self.request.user not in cart.group.members.all():
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

            # if cart is confirmed we will throw an error. (means vote is complete)
            if cart.is_confirmed:
                return Response(status=status.HTTP_423_LOCKED)

            product = Product.objects.create(
                cart=cart,
                title=serializer.validated_data["title"],
                description=serializer.validated_data["description"],
                price=serializer.validated_data["price"],
                count=serializer.validated_data["count"], )
            product_price = product.price * product.count
            cart.total_price += product_price
            cart.save()
            serializer = ProductSerializer(product)
            return Response(serializer.data, status.HTTP_200_OK)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        serializer = ProductUpdateSerializer(data=request.data)
        if serializer.is_valid():
            product = get_object_or_404(Product, id=serializer.validated_data["id"])
            cart = get_object_or_404(Cart, id=product.cart.id)

            # throw an error if user is not in cart users
            if self.request.user not in cart.users.all():
                return Response(status=status.HTTP_403_FORBIDDEN)

            # throw an error if user is not in group
            if self.request.user not in cart.group.members.all():
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

            # if cart is confirmed we will throw an error. (means vote is complete)
            if cart.is_confirmed:
                return Response(status=status.HTTP_423_LOCKED)

            # update the cart pricing
            cart.total_price -= (product.price * product.count)
            cart.total_price += (serializer.validated_data["price"] * serializer.validated_data["count"])
            cart.save()

            serializer.instance = product
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        product_id = self.request.query_params.get("id", None)
        if not product_id:
            return Response({"message": "please give an id"}, status=status.HTTP_400_BAD_REQUEST)
        product = get_object_or_404(Product, id=product_id)

        # check if user is in cart
        if self.request.user not in product.cart.users.all():
            return Response(status=status.HTTP_403_FORBIDDEN)

        product_total_price = product.price * product.count
        cart = get_object_or_404(Cart, id=product.cart.id)

        # if cart is confirmed we will throw an error. (means vote is complete)
        if cart.is_confirmed:
            return Response(status=status.HTTP_423_LOCKED)
        cart.total_price -= product_total_price
        cart.save()
        product.delete()
        return Response({"message": "Product has been deleted"}, status=status.HTTP_200_OK)


class VoteCartView(APIView):
    """
    POST: make a vote for a cart if vote get complete cart will get confirm
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = VoteCartSerializer(data=request.data)
        if serializer.is_valid():
            cart = get_object_or_404(Cart, id=serializer.validated_data["cart"])

            # check if user is in group
            if self.request.user not in cart.group.members.all():
                return Response(status=status.HTTP_404_NOT_FOUND)

            # check if user is in cart users
            if self.request.user not in cart.users.all():
                return Response(status=status.HTTP_403_FORBIDDEN)

            # if cart is confirmed we will throw an error. (means vote is complete)
            if cart.is_confirmed:
                return Response(status=status.HTTP_423_LOCKED)

            # if with this new vote cart vote will complete then
            # we delete all the votes and confirm the cart
            votes = CartVote.objects.filter(cart=cart)

            # if user is already vote throw a 409 error
            if votes.filter(owner=self.request.user).count() >= 1:
                return Response(status=status.HTTP_409_CONFLICT)

            votes_counts = votes.count() + 1

            if votes_counts >= cart.group.members.all().count():
                CartVote.objects.filter(cart=cart).delete()
                cart.is_confirmed = True
                cart.save()
                return Response(status=status.HTTP_202_ACCEPTED)

            CartVote.objects.create(
                owner=self.request.user,
                cart=cart,
                description=serializer.validated_data["description"],
            )
            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
