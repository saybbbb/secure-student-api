from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import login_view, PaymentViewSet

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('login/', login_view, name='rate-limited-login'),
    path('', include(router.urls)),
]
