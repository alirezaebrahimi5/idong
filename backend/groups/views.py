from django.shortcuts import get_object_or_404
from django.db import transaction

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import GroupAllSerializer, GroupCreateSerializer, GroupUpdateSerializer
from .models import Group


class GroupListCreateView(APIView):
    """
    GET: Shows all groups user is joined
    POST: Create a new group (Gets: title, image)
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        groups = Group.objects.filter(members__in=[request.user])
        serializer = GroupAllSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = GroupCreateSerializer(data=request.data)
        if serializer.is_valid():
            # create a new group and then add user it self to group
            Group.objects.create(title=serializer.validated_data["title"],
                                 image=serializer.validated_data["image"]).members.add(request.user)
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupUpdateDeleteDetailView(APIView):
    """
    GET: shows Detail of the user
    PUT: Update a group (can get title, image)
    DELETE: Delete a group"""
    def get(self, request, group_id: int):
        group = get_object_or_404(Group, id=group_id, members__in=[request.user])
        serializer = GroupAllSerializer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, group_id: int):
        serializer = GroupUpdateSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            group = get_object_or_404(Group, id=group_id, members__in=[request.user])
            serializer.instance = group
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, group_id: int):
        # TODO: think about that if we need a vote for group delete
        pass


class GroupInviteView(APIView):
    """
    GET: Create a link for given group id in query params
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        group_id = self.request.query_params.get("group", None)
        if not group_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        group = get_object_or_404(Group, id=group_id, members__in=[request.user])
        # TODO make a .env and put domain inside it
        # make a link and send to client
        link = "http://127.0.0.1:8000/group/join/?code={}".format(group.code)
        return Response({"link": link}, status=status.HTTP_200_OK)


class GroupJoinView(APIView):
    """
    GET: gets a group's code and join user to that group
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        code = self.request.query_params.get("code", None)
        if not code:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        group = get_object_or_404(Group, code=code)
        # if user is already joined send an error
        if self.request.user in group.members.all():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        group.members.add(request.user)
        group.save()
        return Response(status=status.HTTP_200_OK)
