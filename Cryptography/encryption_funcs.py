import base64
from typing import Callable

from Crypto.Cipher import AES
import config


def get_encryption_key() -> bytes:
    secret_key = config.secret_key_for_encryption
    return base64.urlsafe_b64decode(secret_key)


def encrypt_string(text: str, get_key_func: Callable[[], bytes]) -> str:
    cipher = AES.new(get_key_func(), AES.MODE_GCM)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(text.encode())
    return base64.b64encode(nonce + tag + ciphertext).decode()


def decrypt_string(encrypted_text: str, get_key_func: Callable[[], bytes]) -> str:
    encrypted_text_bytes = base64.b64decode(encrypted_text.encode())
    nonce, tag, ciphertext = encrypted_text_bytes[:16], encrypted_text_bytes[16:32], encrypted_text_bytes[32:]
    cipher = AES.new(get_key_func(), AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode()


class Crypto:

    def encrypt(self, string: str):
        return encrypt_string(string, get_encryption_key)

    def decrypt(self, string: str):
        return decrypt_string(string, get_encryption_key)


# instantiate
crypto = Crypto()
