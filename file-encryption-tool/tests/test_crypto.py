import pytest
from backend.crypto_utils import DecryptionError, decrypt_bytes, encrypt_bytes


def test_round_trip():
    data = b"hello secret world" * 100
    assert decrypt_bytes(encrypt_bytes(data, "StrongPass1"), "StrongPass1") == data


def test_wrong_password():
    blob = encrypt_bytes(b"data", "StrongPass1")
    with pytest.raises(DecryptionError):
        decrypt_bytes(blob, "WrongPass")


def test_tampered_file():
    blob = bytearray(encrypt_bytes(b"data", "StrongPass1"))
    blob[-1] ^= 1
    with pytest.raises(DecryptionError):
        decrypt_bytes(bytes(blob), "StrongPass1")
