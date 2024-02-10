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
    """
    permission_classes = (IsAuthenticated,)

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
            users_len = len(serializer.validated_data["users"]) + 1

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
            return Response(CartSerializer(cart).data, status.HTTP_200_OK)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

