from rest_framework import views
from rest_framework.permissions import IsAuthenticated

from backend_ecommerce.helpers import custom_response
from user.serializers import UserProfileSerializer


class UserProfileView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(request.user)
        return custom_response("Get user successfully!", "Success", serializer.data, 200)

    def put(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return custom_response("Update user successfully!", "Success", serializer.data, 200)
        return custom_response("Update user failed!", "Error", serializer.errors, 400)
