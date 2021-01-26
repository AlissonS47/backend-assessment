from rest_framework import viewsets, status
from django.contrib.auth.models import User
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer


class UserRegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = UserRegistrationSerializer
    http_method_names = ['post']

    def create(self, request):
        user = UserRegistrationSerializer(data=request.data)
        response_status = status.HTTP_201_CREATED
        response_message = {"Success": "User successfully created"}
        if user.is_valid():
            try:
                user.save()
            except Exception:
                response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
                response_message = {"Failed": "Internal Server Error"}
        else:
            response_status = status.HTTP_422_UNPROCESSABLE_ENTITY
            response_message = {"Failed": user.errors}
        return Response(data=response_message, status=response_status)
