from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from core.serializers import UserCreateSerializer, UserSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def whoami(request):
    if request.method == "GET" and request.user.is_authenticated:
        user = request.user
        serializer = UserSerializer(user)

        data = {"user": serializer.data}

        return Response(data)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def user_list(request):
    if request.method == "GET":
        users = User.objects.all()
        serializer = UserSerializer(instance=users, many=True)

        data = {"users": serializer.data}

        return Response(data)
    elif request.method == "POST":
        serializer = UserCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            data = {"message": "User created", "user": serializer.data}

            return Response(data, status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = UserSerializer(user)

        data = {"user": serializer.data}

        return Response(data)
    elif request.method == "PATCH":
        serializer = UserCreateSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            data = {"message": "User updated", "user": serializer.data}
            return Response(data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        user.delete()

        data = {"message": "user deleted"}

        return Response(data, status=status.HTTP_204_NO_CONTENT)
