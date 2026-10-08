from core.chaos_engine import ChaosEngine
from core.crypto_engine import CryptoEngine
from utils.file_handler import FileHandler
import hashlib
import struct
import zlib

def create_fake_png(payload):
    png = b'\x89PNG\r\n\x1a\n'

    # IHDR (1x1 image)
    ihdr_data = struct.pack(">IIBBBBB",
                            1, 1, 8, 2, 0, 0, 0)
    ihdr = b'IHDR' + ihdr_data
    png += struct.pack(">I", len(ihdr_data)) + ihdr + struct.pack(">I", zlib.crc32(ihdr) & 0xffffffff)

    # IDAT
    raw_data = b'\x00\x00\x00'
    compressed = zlib.compress(raw_data)
    idat = b'IDAT' + compressed
    png += struct.pack(">I", len(compressed)) + idat + struct.pack(">I", zlib.crc32(idat) & 0xffffffff)

    # IEND
    iend = b'IEND'
    png += struct.pack(">I", 0) + iend + struct.pack(">I", zlib.crc32(iend) & 0xffffffff)

    # 🔥 Append encrypted payload
    # png += payload
    png += b'STEALTH_START' + payload

    return png

class ImageEncryptor:

    def __init__(self, password):
        self.password = password.encode()

        # 🔥 Proper seed derivation (RIGHT PLACE)
        seed = int.from_bytes(
            hashlib.sha256(self.password).digest()[:8],
            'big'
        )

        self.chaos = ChaosEngine(seed)
        self.crypto = CryptoEngine(password)
        self.file = FileHandler()

    def encrypt(self, input_path, output_path):
        arr, mode, format = self.file.load_image(input_path)
        shape = arr.shape

        arr = self.chaos.permute(arr)
        arr = self.chaos.diffuse(arr)

        encrypted = self.crypto.encrypt(arr.tobytes(), shape, mode, format)

        with open(output_path, 'wb') as f:
            f.write(encrypted)

    def decrypt(self, input_path, output_path):
        with open(input_path, 'rb') as f:
            blob = f.read()

        raw, shape, mode, format = self.crypto.decrypt(blob)

        import numpy as np
        arr = np.frombuffer(raw, dtype=np.uint8).reshape(shape)

        # 🔥 IMPORTANT: reverse order
        arr = self.chaos.inverse_diffuse(arr)
        arr = self.chaos.inverse_permute(arr)

        self.file.save_image(arr, output_path, mode, format)


import os

def menu():
    print("\n==== Image Encryption Tool ====")
    print("1. Encrypt Image")
    print("2. Decrypt Image")
    print("3. Exit")

def get_choice():
    return input("Choose an option: ").strip()

def confirm_delete():
    choice = input("Do you want to delete the original image for security purposes? (y/n): ").lower()
    return choice in ["y", "yes"]

def main():
    password = input("Enter password: ")
    tool = ImageEncryptor(password)

    while True:
        menu()
        choice = get_choice()

        if choice == "1":
            input_path = input("Enter image path: ").strip()
            stealth = input("Enable stealth mode? (y/n): ").lower() in ["y", "yes"]

            if stealth:
                output_path = input("Enter output file name (e.g., image.png): ").strip()
            else:
                output_path = input("Enter output encrypted file name (e.g., vault.enc): ").strip()

            if not os.path.exists(input_path):
                print("[!] File not found.")
                continue

            delete_original = confirm_delete()

            tool.encrypt(input_path, output_path)

            if stealth:
                with open(output_path, "rb") as f:
                    data = f.read()

                # 🧠 Fake PNG header (valid signature)
                fake_png = create_fake_png(data)

                with open(output_path, "wb") as f:
                    f.write(fake_png)

                print("[+] Stealth mode applied (disguised as PNG)")
            print("[+] Encryption complete.")

            if delete_original:
                try:
                    os.remove(input_path)
                    print("[+] Original image deleted.")
                except Exception as e:
                    print("[!] Failed to delete original:", e)

        elif choice == "2":
            input_path = input("Enter encrypted file path: ").strip()

            if not os.path.exists(input_path):
                print("[!] File not found.")
                continue

            # 🔥 Auto original filename restore
            original_name = input("Enter original file name to restore (e.g., image.png): ").strip()

            try:
                with open(input_path, "rb") as f:
                    blob = f.read()

                # 🧠 Detect stealth PNG
                if b'STEALTH_START' in blob:
                    print("[*] Stealth PNG detected. Extracting payload...")

                    marker_index = blob.find(b'STEALTH_START')
                    blob = blob[marker_index + len(b'STEALTH_START'):]

                # Save temp cleaned file
                temp_path = "__temp.enc"
                with open(temp_path, "wb") as f:
                    f.write(blob)

                tool.decrypt(temp_path, original_name)

                os.remove(temp_path)
                
                print(f"[+] Decryption complete. Saved as {original_name}")
            except Exception:
                print("[!] Decryption failed. Incorrect password or corrupted file.")

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("[!] Invalid choice. Try again.")

if __name__ == "__main__":
    main()