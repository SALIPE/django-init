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



