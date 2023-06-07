import hashlib
import hmac
import secrets


def hash(password):
    return hmac.new(b"UBIytFgUgfwdgbsuy", password.encode(), hashlib.sha256).hexdigest()


def generate_session():
    return secrets.token_urlsafe(16)
