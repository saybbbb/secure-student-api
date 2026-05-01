from cryptography.fernet import Fernet
from django.conf import settings


cipher = Fernet(settings.FERNET_KEY.encode())


def encrypt_data(plain_text: str) -> str:
    return cipher.encrypt(plain_text.encode()).decode()


def decrypt_data(encrypted_text: str) -> str:
    return cipher.decrypt(encrypted_text.encode()).decode()
