from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

import struct

class CryptoEngine:

    def __init__(self, password):
        self.password = password.encode()

    def derive_key(self, salt):
        return PBKDF2(self.password, salt, dkLen=32, count=300000)

    def encrypt(self, data, shape, mode, format):
        salt = get_random_bytes(16)
        key = self.derive_key(salt)

        cipher = AES.new(key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(data)

        h, w = shape[:2]
        c = shape[2] if len(shape) == 3 else 1

        mode_bytes = mode.encode().ljust(10)
        format_bytes = format.encode().ljust(10)

        metadata = struct.pack("III", h, w, c) + mode_bytes + format_bytes

        return metadata + salt + cipher.nonce + tag + ciphertext

    def decrypt(self, blob):
        # Extract metadata
        metadata = blob[:32]

        h, w, c = struct.unpack("III", metadata[:12])
        mode = metadata[12:22].decode().strip()
        format = metadata[22:32].decode().strip()

        # ✅ FIXED OFFSETS (shifted by 32 bytes)
        salt = blob[32:48]
        nonce = blob[48:64]
        tag = blob[64:80]
        ciphertext = blob[80:]

        key = self.derive_key(salt)

        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        raw = cipher.decrypt_and_verify(ciphertext, tag)

        return raw, (h, w, c), mode, format