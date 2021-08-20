from rest_framework.response import Response
from .serializers import UserSerializerLogin, UserSerializerRegister
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request, *args, **kwargs):
    serialized_data = UserSerializerLogin(data=request.data)
    if(serialized_data.is_valid(raise_exception=True)):
        data = serialized_data.validated_data
        u = authenticate(email=data.get("email"),
                         password=data.get("password"))
        if u is not None:
            refresh = RefreshToken.for_user(u)
            res = {
                "refresh_token": str(refresh),
                "access_token": str(refresh.access_token),
            }
            return Response(res, status=status.HTTP_200_OK)
        else:
            return Response({"message": "try again"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request, *args, **kwargs):
    serializer = UserSerializerRegister(data=request.data)
    if not serializer.is_valid(raise_exception=True):
        return Response({"message": "BadRequest made, Try again."}, status.HTTP_400_BAD_REQUEST)
    user = serializer.save()
    return Response({"message": "login now!"}, status.HTTP_201_CREATED)


@api_view(["POST"])
@authentication_classes([JWTAuthentication, ])
@permission_classes([IsAuthenticated])
def logout(request, *args, **kwargs):
    try:
        refresh_token = request.data["refresh_token"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "logged out successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)