import hashlib
import hmac
import secrets
import json

try:
    with open("config.json", 'r') as file:
        data = json.load(file)
        key = data["key"]

except Exception as e:
    exit("Incorrect config file")


def hash(password):
    return hmac.new(bytes(key, encoding='utf-8'), password.encode(), hashlib.sha256).hexdigest()


def generate_session():
    return secrets.token_urlsafe(16)
