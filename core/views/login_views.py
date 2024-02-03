from django.contrib.auth.models import User
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import exceptions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.serializers import UserSerializer
from core.utils.generate_tokens import (generate_access_token,
                                        generate_refresh_token)


@api_view(["POST"])
@ensure_csrf_cookie
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    response = Response()

    if (username is None) or (password is None):
        raise exceptions.AuthenticationFailed("username and password required")
    user = User.objects.filter(username=username).first()

    if user is None:
        raise exceptions.AuthenticationFailed("user not found")
    if not user.check_password(password):
        raise exceptions.AuthenticationFailed("wrong password")

    serializer_user = UserSerializer(user).data

    access_token, expiry = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    response.set_cookie(key="refreshtoken", value=refresh_token, httponly=True)
    response.data = {
        "token": access_token,
        "refresh_token": refresh_token,
        "expiry": expiry,
        "user": serializer_user,
    }

    return response
