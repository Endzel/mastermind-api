from django.contrib.auth import login, authenticate

from rest_framework import status, generics, mixins
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from mastermind.serializers import CreateUserSerializer


class RetrieveTokenView(generics.GenericAPIView):

    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.data.get("username"), password=request.data.get("password"))
        if not user:
            return Response({"error": "Incorrect login"}, status=status.HTTP_401_UNAUTHORIZED)
        login(request, user)
        token = Token.objects.get(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)


class CreateUserView(mixins.CreateModelMixin,
                    generics.GenericAPIView):

    permission_classes = (AllowAny,)
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
