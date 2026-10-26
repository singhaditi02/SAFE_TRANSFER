# File Encryption & Decryption Tool
Python (FastAPI + cryptography) backend, JavaScript frontend. AES-256-GCM with a password-derived key.

## Run in VS Code
1. Open this folder: File > Open Folder.
2. Terminal > New Terminal, then:
   - Windows: `python -m venv venv` then `venv\Scripts\activate`
   - macOS/Linux: `python3 -m venv venv` then `source venv/bin/activate`
3. `pip install -r requirements.txt`
4. `uvicorn backend.main:app --reload`
5. Open http://127.0.0.1:8000

## CLI
    python cli.py encrypt myfile.pdf
    python cli.py decrypt myfile.pdf.enc

## Tests
    pip install pytest
    pytest

## Files
| File | Purpose |
|---|---|
| backend/config.py | settings (size limit, KDF rounds) |
| backend/crypto_utils.py | encryption/decryption logic |
| backend/main.py | FastAPI API + serves the UI |
| frontend/index.html | page structure |
| frontend/style.css | styling |
| frontend/app.js | UI behavior, calls the API |
| cli.py | command-line interface |
| tests/test_crypto.py | automated tests |
| requirements.txt | dependencies |

Keep your password safe: without it, files cannot be recovered.
