from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser
from .models import EdgeNode

class EdgeNodeAPIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get('X-API-KEY')
        if not api_key:
            return None
        try:
            edge_node = EdgeNode.objects.get(api_key=api_key)
        except EdgeNode.DoesNotExist:
            raise AuthenticationFailed('Invalid API Key')
        request.edge_node = edge_node
        return (AnonymousUser(), None)