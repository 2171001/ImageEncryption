# 🔐 Image Encryption Toolkit

A cybersecurity-focused image encryption tool that protects visual data from unauthorized access and tampering using a combination of **chaos-based pixel transformation** and **AES-GCM authenticated encryption**.

The toolkit provides an interactive command-line interface for encrypting and decrypting image files, with optional original-file deletion and a stealth mode for disguising encrypted payloads as PNG files.

---

## 🛡️ Features

- 🔐 **AES-GCM Encryption**
  - Provides confidentiality and authenticated encryption.
  - Detects incorrect passwords and modified encrypted data.

- 🧬 **Chaos-Based Image Transformation**
  - Performs deterministic pixel permutation.
  - Applies XOR-based pixel diffusion before cryptographic encryption.

- 🖼️ **Multiple Image Formats**
  - Works with common image formats supported by Pillow, including:
    - PNG
    - JPG / JPEG
    - BMP
    - GIF
    - TIFF
    - WEBP
    - and other Pillow-supported formats.

- 🔓 **Image Decryption**
  - Automatically reconstructs the original image dimensions and pixel representation from encrypted metadata.

- 🕵️ **Stealth Mode**
  - Packages the encrypted payload behind a valid PNG structure.
  - Allows the encrypted file to appear as a PNG while retaining the encrypted payload for the toolkit to recover.

- 🗑️ **Optional Original Image Deletion**
  - Before encryption, the user is explicitly asked whether the original image should be deleted.
  - The original file is deleted only when the user confirms with `y` or `yes`.

- 💻 **Interactive CLI**
  - Every encryption and decryption operation requires explicit user interaction.
  - The tool does not automatically encrypt or decrypt files when started.

- 🔑 **Password-Based Key Derivation**
  - Derives the AES key from the user's password using PBKDF2 and a randomly generated salt.

- 🧪 **Integrity Protection**
  - AES-GCM authentication detects incorrect passwords and ciphertext tampering.

---

## 🧠 How It Works

The encryption process combines image-level transformation with authenticated cryptography.

### Encryption

```text
Original Image
      │
      ▼
Load Image Pixels
      │
      ▼
Chaos-Based Permutation
      │
      ▼
Pixel Diffusion
      │
      ▼
PBKDF2 Key Derivation
      │
      ▼
AES-GCM Encryption
      │
      ▼
Encrypted Payload
      │
      ├── Normal Mode → Encrypted File
      │
      └── Stealth Mode → PNG-disguised Encrypted File
````

### Decryption

```text
Encrypted File
      │
      ▼
Stealth Payload Detection
      │
      ▼
AES-GCM Authentication & Decryption
      │
      ▼
Reverse Pixel Diffusion
      │
      ▼
Reverse Chaos Permutation
      │
      ▼
Reconstructed Image
```

---

## 🔬 Cryptographic Components

### AES-GCM

The encrypted pixel data is protected using **AES in Galois/Counter Mode (GCM)**.

AES-GCM provides:

* Confidentiality
* Authentication
* Integrity verification

A modified encrypted file or incorrect password causes authenticated decryption to fail.

---

### PBKDF2

The user's password is not directly used as the AES key.

Instead, the toolkit derives a 256-bit key using:

```text
Password + Random Salt
        │
        ▼
      PBKDF2
        │
        ▼
   256-bit AES Key
```

The encryption process generates a fresh random salt for each encryption operation.

---

### Chaos-Based Transformation

Before AES-GCM encryption, the image's pixel array undergoes two reversible transformations:

#### 1. Permutation

Pixels are rearranged using a deterministic pseudo-random permutation derived from the password.

#### 2. Diffusion

The pixel data is XORed with a deterministic pseudo-random byte sequence.

During decryption, these operations are reversed in the correct order to reconstruct the original pixel array.

---

## 🕵️ Stealth Mode

Stealth mode provides an additional layer of file disguise.

Instead of producing a conventional encrypted file such as:

```text
image.enc
```

the encrypted payload can be packaged behind a valid PNG structure:

```text
secret.png
```

The resulting file contains:

```text
PNG Structure
     +
Stealth Marker
     +
Encrypted Payload
```

The toolkit recognizes its own stealth marker and extracts the encrypted payload before attempting AES-GCM decryption.

> **Note:** Stealth mode is file-format masquerading, not cryptographic protection by itself. The security of the encrypted payload comes from the encryption layer.

---

## 🚀 Requirements

Before running the project, make sure you have:

* Python 3.13 or newer
* Poetry
* Git

The project dependencies are managed through Poetry.

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
```

Enter the project directory:

```bash
cd YOUR-REPOSITORY
```

Install the dependencies using Poetry:

```bash
poetry install
```

Poetry will create and manage the project's isolated environment and install the dependencies defined by the project.

---

## ▶️ Running the Tool

Start the toolkit with:

```bash
poetry run python main.py
```

The program starts in interactive mode and waits for the user's selection.

You will see:

```text
==== Image Encryption Tool ====
1. Encrypt Image
2. Decrypt Image
3. Exit
Choose an option:
```

Nothing is encrypted or decrypted automatically.

---

# 🔐 Encrypting an Image

Select:

```text
1. Encrypt Image
```

The toolkit asks for the image path:

```text
Enter image path:
```

Next, choose whether to enable stealth mode:

```text
Enable stealth mode? (y/n):
```

Then provide the output filename.

For normal encryption:

```text
Enter output encrypted file name (e.g., vault.enc):
```

For stealth encryption:

```text
Enter output file name (e.g., image.png):
```

Before encryption begins, the toolkit asks:

```text
Do you want to delete the original image for security purposes? (y/n):
```

### `y` / `yes`

The image is encrypted and the original file is deleted after successful encryption.

### `n` / `no`

The original image remains untouched.

---

# 🔓 Decrypting an Image

Select:

```text
2. Decrypt Image
```

Enter the encrypted file:

```text
Enter encrypted file path:
```

Then provide the filename that should be used for the reconstructed image:

```text
Enter original file name to restore (e.g., image.png):
```

For example:

```text
Enter encrypted file path: image.enc
Enter original file name to restore (e.g., image.png): restored.png
```

The toolkit reconstructs the image using the metadata stored during encryption.

---

## 🔑 Password Protection

The same password used during encryption must be supplied when decrypting the encrypted file.

For example:

```text
Enter password: MyStrongPassword
```

Using an incorrect password causes AES-GCM authentication to fail.

The toolkit reports:

```text
[!] Decryption failed. Incorrect password or corrupted file.
```

---

## 🛡️ Tamper Detection

AES-GCM also protects the encrypted payload against unauthorized modification.

If an attacker modifies the encrypted data, authenticated decryption fails instead of silently producing corrupted image data.

This provides an important distinction:

```text
Encryption
    ↓
Confidentiality
```

and:

```text
AES-GCM Authentication
    ↓
Integrity + Authenticity
```

---

## 🧪 Testing

A basic encryption/decryption test can be executed with:

```bash
poetry run python tests/test_encryption.py
```

A successful test produces:

```text
Test completed.
```

You can also manually verify pixel-level recovery using Python:

```python
from PIL import Image
import numpy as np

original = np.array(Image.open("image.jpg"))
restored = np.array(Image.open("restored.jpg"))

print("Pixel match:", np.array_equal(original, restored))
```

Expected result:

```text
Pixel match: True
```

### Why `cmp` May Report Differences

The following command may report that two files differ:

```bash
cmp image.jpg restored.jpg
```

This does not necessarily mean that the image content was incorrectly decrypted.

The toolkit reconstructs the image from its pixel representation rather than preserving the original file's exact binary encoding.

Therefore:

```text
Pixel data
    → can be identical
```

while:

```text
Original file bytes
    → can differ from reconstructed file bytes
```

The pixel-level comparison is therefore the appropriate test for verifying reconstructed image content in this implementation.

---

## 🔎 Security Testing

### Wrong Password

Attempt to decrypt an encrypted image using an incorrect password.

Expected behavior:

```text
[!] Decryption failed. Incorrect password or corrupted file.
```

No decrypted image should be produced from the failed authentication attempt.

---

### Encrypted File Tampering

Modify the encrypted payload and attempt decryption again.

Expected behavior:

```text
[!] Decryption failed. Incorrect password or corrupted file.
```

This demonstrates AES-GCM authentication detecting ciphertext modification.

---

### Normal Image vs. Stealth File

The toolkit distinguishes its stealth files using its own stealth marker rather than simply assuming that every PNG file is a stealth file.

This prevents ordinary PNG images from being incorrectly classified as stealth-encrypted files.

---

## ⚠️ Important Notes

### Keep Your Password Safe

The encryption password is required for decryption.

If the password is lost, the encrypted image cannot be recovered through the normal decryption process.

### Secure Deletion

The optional deletion feature removes the original file from the filesystem after encryption.

However, deleting a file does not guarantee forensic destruction of every underlying storage block, especially on modern filesystems, SSDs, copy-on-write filesystems, or systems with backups/snapshots.

### Stealth Mode Is Not a Replacement for Encryption

Stealth mode disguises the encrypted payload's file representation.

It does not replace AES-GCM encryption.

The actual confidentiality of the image comes from the cryptographic encryption layer.

---

## 💻 Example Session

```text
Enter password: MyStrongPassword

==== Image Encryption Tool ====
1. Encrypt Image
2. Decrypt Image
3. Exit
Choose an option: 1

Enter image path: image.jpg
Enable stealth mode? (y/n): n
Enter output encrypted file name (e.g., vault.enc): image.enc

Do you want to delete the original image for security purposes? (y/n): n

[+] Encryption complete.
```

Decryption:

```text
==== Image Encryption Tool ====
1. Encrypt Image
2. Decrypt Image
3. Exit
Choose an option: 2

Enter encrypted file path: image.enc
Enter original file name to restore (e.g., image.png): restored.jpg

[+] Decryption complete. Saved as restored.jpg
```

---

## 🧰 Technologies Used

* **Python**
* **Poetry**
* **NumPy**
* **Pillow**
* **PyCryptodome**
* **AES-GCM**
* **PBKDF2**
* **Deterministic pseudo-random permutation**
* **XOR-based pixel diffusion**

---

## ⚖️ Disclaimer

This project is intended for **educational, cybersecurity research, and authorized security testing purposes**.

Do not use this tool to encrypt or delete files that you do not own or have explicit authorization to modify.

Always maintain appropriate backups of important data before testing encryption or deletion functionality.
