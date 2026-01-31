# src/hashing.py
import hashlib
import os

def sha256(path: str):
    if not path or not os.path.isfile(path):
        return None

    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(4096), b""):
            h.update(b)
    return h.hexdigest()
