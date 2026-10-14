"""Signed webhook payloads; callers must configure allowlisted destinations."""
import hashlib,hmac,json
from urllib.parse import urlparse
def sign(payload:dict,secret:str):
    body=json.dumps(payload,sort_keys=True,separators=(',',':')).encode()
    return hmac.new(secret.encode(),body,hashlib.sha256).hexdigest()
def validate_destination(url:str,allowed_hosts:set[str]):
    parsed=urlparse(url)
    if parsed.scheme!='https' or parsed.hostname not in allowed_hosts or parsed.username or parsed.password:raise ValueError('Webhook destination not allowlisted')
    return url
