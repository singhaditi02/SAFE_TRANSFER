"""FastAPI web server: exposes /api/encrypt and /api/decrypt and serves the UI."""
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles

from .config import ENCRYPTED_EXT, FRONTEND_DIR, MAX_FILE_SIZE_MB
from .crypto_utils import DecryptionError, decrypt_bytes, encrypt_bytes

app = FastAPI(title="File Encryption & Decryption Tool")


async def _read_upload(file: UploadFile) -> bytes:
    data = await file.read()
    if len(data) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(413, f"File is larger than {MAX_FILE_SIZE_MB} MB.")
    if not data:
        raise HTTPException(400, "The file is empty.")
    return data


def _download(data: bytes, name: str) -> Response:
    return Response(
        content=data,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{name}"'},
    )


@app.post("/api/encrypt")
async def encrypt(file: UploadFile = File(...), password: str = Form(...)):
    if len(password) < 8:
        raise HTTPException(400, "Password must be at least 8 characters.")
    data = await _read_upload(file)
    return _download(encrypt_bytes(data, password), file.filename + ENCRYPTED_EXT)


@app.post("/api/decrypt")
async def decrypt(file: UploadFile = File(...), password: str = Form(...)):
    data = await _read_upload(file)
    try:
        plain = decrypt_bytes(data, password)
    except DecryptionError as e:
        raise HTTPException(400, str(e))
    name = file.filename
    name = name[: -len(ENCRYPTED_EXT)] if name.endswith(ENCRYPTED_EXT) else name + ".decrypted"
    return _download(plain, name)


# Must be last: serves index.html, style.css, app.js
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
