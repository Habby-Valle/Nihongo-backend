import datetime

import jwt
from django.conf import settings


def generate_access_token(user):
    expiry = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    access_token_payload = {
        "user_id": user.id,
        "username": user.username,
        "exp": expiry,
        "iat": datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(
        access_token_payload, settings.SECRET_KEY, algorithm="HS256"
    )

    return access_token, expiry


def generate_refresh_token(user):
    current_time = datetime.datetime.utcnow()
    expiration_time = current_time + datetime.timedelta(days=30)

    refresh_token_payload = {
        "user_id": user.id,
        "username": user.username,
        "exp": expiration_time,
        "iat": datetime.datetime.utcnow(),
    }

    refresh_token_payload = jwt.encode(
        refresh_token_payload, settings.SECRET_KEY, algorithm="HS256"
    )

    return refresh_token_payload
