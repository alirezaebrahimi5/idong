from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import AnonRateThrottle

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from .serializers import *
from .models import CustomUser as User
from .models import *


class CustomThrottle(AnonRateThrottle):
    rate = '1/s'

    def parse_rate(self, rate):
        return (10, 60)


class SendEmailView(APIView):
    """
    gets an email and name creates a used then sends a code to email
    """

    permission_classes = (AllowAny,)
    # throttle_classes = (CustomThrottle,)

    def post(self, request):
        serializer = LoginSignupSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            # if there is a user with given email it will send bad request
            user, created = CustomUser.objects.get_or_create(email=serializer.validated_data["email"],)
            if not created:
                # if code exist check create count if not just create a one and email it
                try:
                    code = LoginCode.objects.get(user=user)
                except LoginCode.DoesNotExist:
                    code = LoginCode.create_token(user)
                    # here we send email
                    print("Code: " + str(code))
                    return Response(status=status.HTTP_201_CREATED)
                if code.wait_until:
                    time_difference = timezone.now() - code.wait_until
                    if time_difference.total_seconds() / 60 <= 1:
                        return Response({"message": "Wait"}, status=status.HTTP_406_NOT_ACCEPTABLE)
                    else:
                        code.wait_until = None
                        code.create_count = 0

                # increase create_count and if its used 2 times or more we make a wait time for the next
                code.create_count += 1
                if code.create_count >= 2:
                    code.wait_until = timezone.now()
                code.save()
                print("Code: " + str(code.code))
                return Response(status=status.HTTP_201_CREATED)

            code = LoginCode.create_token(user)
            # here we send email
            print("Code: " + str(code))
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    gets an email and code if user is inactive it will activate it
    """

    permission_classes = (AllowAny,)

    def post(self, request):
        # we get email and code from url and check them
        email = self.request.query_params.get("email", None)
        code = self.request.query_params.get("code", None)
        if not email or not code or len(code) != 6:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # try to get the user
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # try to get LoginCode with given email and code
        try:
            code = LoginCode.objects.get(code=code,
                                         user=user)
        except LoginCode.DoesNotExist:
            # if there is code with given code we try to find code with user and subtract usage_count
            try:
                code = LoginCode.objects.get(user__email=email)
                code.usage_count += 1
                # delete the code if usage_count is zero
                if code.usage_count == 3:
                    code.delete()
            except LoginCode.DoesNotExist:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # we check if the code is expired and delete it if is expired
        time_difference = timezone.now() - code.updated_at
        time_minute = time_difference.total_seconds() / 60  # after 60 min it will expire
        if time_minute >= 5:
            code.delete()
            # we return 406 for front-end to know its expired
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        code.delete()
        access_token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)
        return Response({"access_token": str(access_token),
                             "refresh_token": str(refresh_token)}, status.HTTP_200_OK)
