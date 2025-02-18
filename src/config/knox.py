from datetime import timedelta
from rest_framework.settings import api_settings

REST_KNOX = {
    "AUTH_TOKEN_CHARACTER_LENGTH": 64,  # By default, it is set to 64 characters (this shouldn't need changing).
    "TOKEN_TTL": timedelta(
        hours=10
    ),  # The default is 10 hours i.e., timedelta(hours=10)).
    "USER_SERIALIZER": "knox.serializers.UserSerializer",
    "TOKEN_LIMIT_PER_USER": None,  # By default, this option is disabled and set to None -- thus no limit.
    "AUTO_REFRESH": False,  # This defines if the token expiry time is extended by TOKEN_TTL each time the token is used.
    "EXPIRY_DATETIME_FORMAT": api_settings.DATETIME_FORMAT,
}
