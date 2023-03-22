import hashlib, hmac

def hash(password):
    return hmac.new(b"UBIytFgUgfwdgbsuy", password.encode(), hashlib.sha256).hexdigest()

