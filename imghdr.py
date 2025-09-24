"""Minimal drop-in replacement for the stdlib `imghdr` module.

This implements a small subset of functionality: `what(file, h=None)`
and detects common image types (jpeg, png, gif, webp, bmp, tiff).

Place this file in the project's import path (the project `src/` dir)
so that `import imghdr` resolves here if the stdlib module is not
available (e.g. on Python 3.13 where some modules were removed).

This is a lightweight workaround; the recommended long-term fix is to
use a Python version compatible with Telethon (3.11/3.12) or install
an updated Telethon that doesn't rely on the removed module.
"""
from __future__ import annotations

from typing import Optional

def _read_header(file):
    # file may be a bytes-like object, a file path or a file-like object
    if isinstance(file, (bytes, bytearray)):
        return bytes(file[:64])

    try:
        # If it's a path-like string
        if isinstance(file, str):
            with open(file, 'rb') as f:
                return f.read(64)

        # file-like object
        pos = None
        if hasattr(file, 'read'):
            try:
                pos = file.tell()
            except Exception:
                pos = None
            header = file.read(64)
            try:
                if pos is not None:
                    file.seek(pos)
            except Exception:
                pass
            return header
    except Exception:
        return b''

    return b''


def what(file, h: Optional[bytes] = None) -> Optional[str]:
    """Return a string describing the image type, like the stdlib `imghdr.what()`.

    Recognizes: 'jpeg', 'png', 'gif', 'webp', 'bmp', 'tiff'.
    Returns None if unknown.
    """
    if h is None:
        header = _read_header(file) or b''
    else:
        header = h[:64]

    if not header:
        return None

    # JPEG
    if header.startswith(b'\xff\xd8\xff'):
        return 'jpeg'

    # PNG
    if header.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'png'

    # GIF
    if header.startswith(b'GIF87a') or header.startswith(b'GIF89a'):
        return 'gif'

    # WEBP (RIFF....WEBP)
    if header[0:4] == b'RIFF' and header[8:12] == b'WEBP':
        return 'webp'

    # BMP (BM)
    if header.startswith(b'BM'):
        return 'bmp'

    # TIFF (II* or MM*)
    if header.startswith(b'II') and header[2:4] == b'*\x00':
        return 'tiff'
    if header.startswith(b'MM') and header[2:4] == b'\x00*':
        return 'tiff'

    return None


__all__ = ['what']
