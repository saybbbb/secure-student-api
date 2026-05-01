from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'cardholder_name', 'amount', 'created_at')
    list_filter = ('created_at',)
