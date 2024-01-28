from base64 import b64decode, b64encode

from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


def decrypt(encrypted_data: str, key):
    encrypted_data = b64decode(encrypted_data)
    iv = encrypted_data[: AES.block_size]
    cipher_text = encrypted_data[AES.block_size :]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_text = cipher.decrypt(cipher_text)
    decrypted_text = unpad(decrypted_text, 16)

    return decrypted_text.decode("utf-8")


def encrypt(plain_text: str, key):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_text = pad(plain_text.encode("utf-8"), 16)
    cipher_text = cipher.encrypt(padded_text)
    encrypted_data = b64encode(iv + cipher_text).decode("utf-8")

    return encrypted_data


