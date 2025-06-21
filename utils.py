import base64
import hashlib
from io import BytesIO
from PIL import Image
from cryptography.fernet import Fernet

def load_image(uploaded_file):
    return Image.open(uploaded_file)

def resize_image(img, max_size=(800, 800)):
    img.thumbnail(max_size)
    return img

def image_to_bytes(img):
    buffer = BytesIO()
    img.save(buffer, format="PNG", optimize=True)
    buffer.seek(0)
    return buffer

def generate_key_from_password(password: str) -> bytes:
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key)

def encrypt_message(message: str, password: str) -> str:
    key = generate_key_from_password(password)
    fernet = Fernet(key)
    encrypted = fernet.encrypt(message.encode())
    return encrypted.decode()

def decrypt_message(encrypted_message: str, password: str) -> str:
    try:
        key = generate_key_from_password(password)
        fernet = Fernet(key)
        decrypted = fernet.decrypt(encrypted_message.encode())
        return decrypted.decode()
    except Exception:
        return None

def calculate_capacity(image):
    width, height = image.size
    return width * height * 3