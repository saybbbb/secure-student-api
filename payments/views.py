import logging
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Payment
from .serializers import PaymentSerializer
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit
import json

logger = logging.getLogger(__name__)


@csrf_exempt
@ratelimit(key='ip', rate='5/m', block=True)
def login_view(request):
    """
    Rate-limited login endpoint.
    Allows max 5 attempts per minute per IP.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    username = data.get('username')
    password = data.get('password')
    user = authenticate(request, username=username, password=password)

    if user is not None:
        logger.info(f"Successful login for user: {username}")
        return JsonResponse({'message': f'Welcome, {username}!'})
    else:
        logger.warning(f"Failed login attempt for user: {username} from IP: {request.META.get('REMOTE_ADDR')}")
        return JsonResponse({'error': 'Invalid credentials'}, status=401)


class PaymentViewSet(viewsets.ModelViewSet):
    """
    Secure Payment API endpoint.
    - Authenticated users can manage their own payments.
    - All actions are logged.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        logger.info(f"Payment created by user: {self.request.user.username}")
        serializer.save(user=self.request.user)
    def perform_destroy(self, instance):
        logger.info(f"Payment #{instance.id} deleted by user: {self.request.user.username}")
        instance.delete()