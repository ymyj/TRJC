from cryptography.fernet import Fernet
from app.config import settings
import bcrypt

_key = settings.ENCRYPTION_KEY.encode().ljust(32)[:32]
from base64 import urlsafe_b64encode
_key = urlsafe_b64encode(_key)
fernet = Fernet(_key)


def encrypt_data(data: str) -> str:
    if not data:
        return data
    return fernet.encrypt(data.encode()).decode()


def decrypt_data(encrypted_data: str) -> str:
    if not encrypted_data:
        return encrypted_data
    try:
        return fernet.decrypt(encrypted_data.encode()).decode()
    except Exception:
        return encrypted_data


def mask_name(name: str) -> str:
    if not name or len(name) == 0:
        return name
    if len(name) == 1:
        return name
    return name[0] + "**"


def mask_phone(phone: str) -> str:
    if not phone or len(phone) < 7:
        return phone
    return phone[:3] + "****" + phone[-4:]


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    if not password or not hashed:
        return False
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
