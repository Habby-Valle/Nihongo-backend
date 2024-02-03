from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Profile
from core.serializers import (ProfileSerializer, ProfileSerializerResponse,
                              ProfileUpdateSerializer)


@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def profile_list(request, user_id):
    try:
        profile = Profile.objects.get(user=user_id)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = ProfileSerializer(profile)

        data = {"profile": serializer.data}

        return Response(data)

    elif request.method == "PATCH":
        serializer = ProfileUpdateSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            updated_profile = Profile.objects.get(user=user_id)
            response_serializer = ProfileSerializer(updated_profile)
            data = {
                "success": "update profile successfully",
                "profile": response_serializer.data,
            }

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
