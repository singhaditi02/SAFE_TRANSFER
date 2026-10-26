"""
Core cryptography logic (no web code here).

Algorithm : AES-256-GCM  (encrypts AND detects tampering / wrong password)
Key       : derived from the password with PBKDF2-HMAC-SHA256 + random salt

Encrypted file layout:
    MAGIC (5) | SALT (16) | NONCE (12) | CIPHERTEXT + AUTH TAG
"""
import os

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from .config import KDF_ITERATIONS, MAGIC, NONCE_SIZE, SALT_SIZE


class DecryptionError(Exception):
    """Raised when decryption fails (wrong password, corrupt or foreign file)."""


def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,                      # 32 bytes = 256-bit key
        salt=salt,
        iterations=KDF_ITERATIONS,
    )
    return kdf.derive(password.encode("utf-8"))


def encrypt_bytes(data: bytes, password: str) -> bytes:
    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)
    key = derive_key(password, salt)
    ciphertext = AESGCM(key).encrypt(nonce, data, MAGIC)
    return MAGIC + salt + nonce + ciphertext


def decrypt_bytes(blob: bytes, password: str) -> bytes:
    header = len(MAGIC) + SALT_SIZE + NONCE_SIZE
    if len(blob) < header + 16 or not blob.startswith(MAGIC):
        raise DecryptionError("This is not a file encrypted by this tool.")
    salt = blob[len(MAGIC): len(MAGIC) + SALT_SIZE]
    nonce = blob[len(MAGIC) + SALT_SIZE: header]
    key = derive_key(password, salt)
    try:
        return AESGCM(key).decrypt(nonce, blob[header:], MAGIC)
    except InvalidTag:
        raise DecryptionError("Wrong password or the file was modified.")
