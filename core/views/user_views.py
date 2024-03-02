from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (AllowAny, BasePermission,
                                        IsAuthenticated)
from rest_framework.response import Response

from core.models import Profile
from core.serializers import ProfileSerializer, UserSerializer


class IsAuthenticatedOrAllowAny(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return IsAuthenticated.has_permission(self, request, view)
        elif request.method == "POST":
            return True
        return False


@api_view(["GET"])
@permission_classes([IsAuthenticatedOrAllowAny])
def whoami(request):
    if request.method == "GET" and request.user.is_authenticated:
        user = request.user
        profile = Profile.objects.get(user=user)
        serializer_user = UserSerializer(user)
        serializer_profile = ProfileSerializer(profile)

        data = {
            "user": serializer_user.data,
            "profile": serializer_profile.data,
        }

        return Response(data)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
