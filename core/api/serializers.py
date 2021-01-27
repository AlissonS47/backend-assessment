from rest_framework import fields, serializers
from core.models import Request


class SuperRequestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Request
        fields = ['id', 'name', 'message', 'checked', 'status']


class SuperRequestUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Request
        fields = ['id', 'name', 'message', 'checked', 'status']
        read_only_fields = ['id', 'name', 'message', 'checked']


class RequestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Request
        fields = ['id', 'message', 'checked', 'status']


class RequestRegistrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Request
        fields = ['message']
    
    def save(self):
        req = Request(
            user = self.context['request'].user,
            message = self.validated_data['message']
        )
        req.save()
        