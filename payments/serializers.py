from rest_framework import serializers
from .models import Payment
from .encryption import encrypt_data, decrypt_data


class PaymentSerializer(serializers.ModelSerializer):
    card_number = serializers.CharField(write_only=True, required=True)
    masked_card = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Payment
        fields = ('id', 'user', 'cardholder_name', 'card_number',
                  'masked_card', 'amount', 'created_at')
        read_only_fields = ('user', 'encrypted_card_number', 'created_at')

    def get_masked_card(self, obj):
        """Decrypt and mask card number for display (show last 4 digits)."""
        try:
            decrypted = decrypt_data(obj.encrypted_card_number)
            return f"****-****-****-{decrypted[-4:]}"
        except Exception:
            return "****-****-****-****"

    def create(self, validated_data):
        card_number = validated_data.pop('card_number')
        validated_data['encrypted_card_number'] = encrypt_data(card_number)
        return super().create(validated_data)
