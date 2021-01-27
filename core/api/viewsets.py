from rest_framework import serializers, viewsets, status
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import (RequestSerializer, SuperRequestSerializer, 
                          SuperRequestUpdateSerializer, 
                          RequestRegistrationSerializer)
from django.core.mail import send_mail
from django.contrib.auth.models import User
from core.models import Request


def send_email(status, email):
    """ Sends an email to the user
    
        Parameters:
        status: status of the user request, can be A(Approved) or R(Rejected)
        email: user's email
    """
    if status == 'R':
        msg = 'Sorry, your request was rejected'
    else:
        msg = 'Congratulations, your request has been approved!'
        
    send_mail('Backend Assessment - Result of your request', msg,
                'django.backend.test@gmail.com', [email], 
                fail_silently=False,)


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = SuperRequestSerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['checked',]
    http_method_names = ['get', 'post', 'patch']
    
    def create(self, request):
        serializer = RequestRegistrationSerializer(
            data=request.data, context={'request': request}
        )
        response_status = status.HTTP_201_CREATED
        if serializer.is_valid():
            try:
                serializer.save()
                response_message = serializer.data
            except:
                response_message = {"Failed": "Internal server error"}
                response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            response_message = {"Failed": serializer.errors}
            response_status = status.HTTP_422_UNPROCESSABLE_ENTITY
        return Response(data=response_message, status=response_status)
    
    def list(self, request):
        if request.user.is_staff:
            request_queryset = self.filter_queryset(Request.objects.all())
            serializer = SuperRequestSerializer(request_queryset, many=True)
        else:
            request_queryset = self.filter_queryset(
                Request.objects.filter(user=request.user.id))
            serializer = RequestSerializer(request_queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        if request.user.is_staff:
            request_queryset = Request.objects.get(id=pk)
            serializer = SuperRequestSerializer(request_queryset)
            return Response(serializer.data)
        else:
            response_message = {"Failed": "Action denied"}
            response_status = status.HTTP_401_UNAUTHORIZED
            return Response(data=response_message, status=response_status)

    def partial_update(self, request, pk=None):
        if request.user.is_staff:
            request_queryset = Request.objects.get(id=pk)
            request_user = User.objects.get(id=request_queryset.user.id)
            serializer = SuperRequestUpdateSerializer(
                request_queryset, data=request.data, partial=True)
            response_status = status.HTTP_200_OK
            if serializer.is_valid():
                try:
                    serializer.save(checked=True)
                    send_email(serializer.data['status'], request_user.email)
                    response_message = serializer.data
                except Exception:
                    response_message = {"Failed": "Internal server error"}
                    response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            else:
                response_message = {"Failed": serializer.errors}
                response_status = status.HTTP_422_UNPROCESSABLE_ENTITY
        else:
            response_message = {"Failed": "Action denied"}
            response_status = status.HTTP_401_UNAUTHORIZED
        return Response(data=response_message, status=response_status)
