from django_ratelimit.decorators import ratelimit

from apps.core.constants.ratelimits import (
    LOGIN,
    PASSWORD_RESET,
    UPLOAD,
    EXCLUIR,
)

def login_rate_limit(view):
    return ratelimit(
        key="ip",
        rate=LOGIN,
        block=True,
    )(view)


def password_reset_rate_limit(view):
    return ratelimit(
        key="user",
        rate=PASSWORD_RESET,
        block=True,
    )(view)

def upload_rate_limit(view):
    return ratelimit(
        key="user",
        rate=UPLOAD,
        block=True,
    )(view)

def excluir_rate_limit(view):
    return ratelimit(
        key="user",
        rate=EXCLUIR,
        block=True,
    )(view)
