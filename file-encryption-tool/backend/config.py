"""Central settings. Change values here, not inside other files."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

MAX_FILE_SIZE_MB = 50          # reject uploads bigger than this
KDF_ITERATIONS = 600_000       # PBKDF2 rounds (slows down password guessing)
MAGIC = b"FENC1"               # marks a file as made by this tool
SALT_SIZE = 16                 # bytes
NONCE_SIZE = 12                # bytes (standard for AES-GCM)
ENCRYPTED_EXT = ".enc"
