from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

# Generate a random 16-byte AES key
aes_key = get_random_bytes(16)

# Save the key to a file for later use in decryption
with open("aes_key.pem", "wb") as key_file:
    key_file.write(aes_key)


def aes_encrypt(message):
    cipher = AES.new(aes_key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return iv + ct


def aes_decrypt(iv_and_ct):
    iv = base64.b64decode(iv_and_ct[:24])
    ct = base64.b64decode(iv_and_ct[24:])
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode()


