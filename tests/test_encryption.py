import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import ImageEncryptor

def test_basic():
    tool = ImageEncryptor("test123")

    tool.encrypt("image.jpg", "test.enc")
    tool.decrypt("test.enc", "restored.png")

    print("Test completed.")

if __name__ == "__main__":
    test_basic()