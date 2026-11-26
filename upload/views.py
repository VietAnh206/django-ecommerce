import cloudinary.uploader
from rest_framework import views

from backend_ecommerce.helpers import IsAdminOrReadOnly, custom_response

from .models import Photo
from .serializers import PhotoSerializer


class PhotoAPIView(views.APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        serializer = PhotoSerializer(Photo.objects.all(), many=True)
        return custom_response("Get all photos successfully!", "Success", serializer.data, 200)

    def post(self, request):
        images = request.FILES.getlist("uploadImages")
        if not images:
            return custom_response("No upload resource", "Error", "No image file found in request", 400)

        data = []
        for image in images:
            try:
                result = cloudinary.uploader.upload(image)
                photo = Photo.objects.create(
                    id=result["public_id"],
                    url=result["secure_url"],
                    filename=result.get("original_filename", ""),
                    format=result.get("format", "png"),
                    width=result["width"],
                    height=result["height"],
                )
                data.append(PhotoSerializer(photo).data)
            except Exception as e:
                return custom_response("Upload images failed!", "Error", [str(e)], 400)
        return custom_response("Upload images successfully!", "Success", data, 200)
