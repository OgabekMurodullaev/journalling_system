from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets


class BaseAPIView(APIView):
    def success_response(self, message, data=None, status_code=status.HTTP_200_OK):
        return Response(
            {
                "success": True,
                "message": message,
                "data": data or {}
            }, status=status_code
        )

    def error_response(self, message, errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        return Response(
            {
                "success": False,
                "message": message,
                "errors": errors or {}
            }, status=status_code
        )


class BaseViewSet(viewsets.ModelViewSet):
    def success(self, message, data=None, status_code=status.HTTP_200_OK):
        return Response({
            "success": True,
            "message": message,
            "data": data or {}
        }, status=status_code)

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return self.success("Ma'lumotlar ro'yxati", serializer.data)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return self.success("Ma'lumot olindi", serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return self.success("Ma'lumot qo'shildi", serializer.data, status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return self.success("Ma'lumot yangilandi", serializer.data)

    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return self.success("Ma'lumot o'chirildi", status_code=status.HTTP_204_NO_CONTENT)