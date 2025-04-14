import base64
from datetime import datetime, timedelta

import jwt

from django.conf import settings

JWT_SECRET = settings.SECRET_KEY
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_DELTA = timedelta(hours=1)

def generate_jwt_token(user):
    payload = {
        'user_id': user.id,  
        'email': user.email,
        'exp': datetime.utcnow() + JWT_EXPIRATION_DELTA,  
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def encrypt_id(value, encryption_key):
    """
    Encrypt the given id using the encryption key.
    The encryption key is concatenated with the id, then Base64-encoded.
    
    :param value: The id to encrypt.
    :param encryption_key: The encryption key (e.g., the table name).
    :return: A string containing the "encrypted" id.
    """
    string_to_encrypt = f"{encryption_key}:{value}"
    encrypted_bytes = base64.urlsafe_b64encode(string_to_encrypt.encode())
    return encrypted_bytes.decode()


def decrypt_id(encrypted_value, encryption_key):
    """
    Decrypts the given encrypted id using the provided encryption key.
    
    :param encrypted_value: The encrypted id string (base64 encoded).
    :param encryption_key: The expected encryption key (e.g., the table name).
    :return: The original id (as a string). You can cast it to int if necessary.
    :raises ValueError: If decryption fails or the encryption key does not match.
    """
    try:
        decoded_bytes = base64.urlsafe_b64decode(encrypted_value.encode())
        decoded_str = decoded_bytes.decode()
        key, value = decoded_str.split(":", 1)
        if key != encryption_key:
            raise ValueError("Encryption key does not match")
        return value
    except Exception as e:
        raise ValueError("Decryption failed") from e
