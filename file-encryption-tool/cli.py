"""Command-line version.  Examples:
    python cli.py encrypt secret.pdf
    python cli.py decrypt secret.pdf.enc
"""
import argparse
import getpass
import sys
from pathlib import Path

from backend.config import ENCRYPTED_EXT
from backend.crypto_utils import DecryptionError, decrypt_bytes, encrypt_bytes


def main() -> None:
    p = argparse.ArgumentParser(description="File Encryption & Decryption Tool")
    p.add_argument("action", choices=["encrypt", "decrypt"])
    p.add_argument("path", type=Path)
    p.add_argument("-o", "--output", type=Path, help="output file (optional)")
    args = p.parse_args()

    if not args.path.is_file():
        sys.exit(f"File not found: {args.path}")
    password = getpass.getpass("Password: ")
    data = args.path.read_bytes()

    if args.action == "encrypt":
        if getpass.getpass("Confirm password: ") != password:
            sys.exit("Passwords do not match.")
        out = args.output or args.path.with_name(args.path.name + ENCRYPTED_EXT)
        out.write_bytes(encrypt_bytes(data, password))
    else:
        try:
            plain = decrypt_bytes(data, password)
        except DecryptionError as e:
            sys.exit(f"Error: {e}")
        default = (args.path.with_suffix("") if args.path.suffix == ENCRYPTED_EXT
                   else args.path.with_name(args.path.name + ".decrypted"))
        out = args.output or default
        out.write_bytes(plain)
    print(f"Done -> {out}")


if __name__ == "__main__":
    main()
