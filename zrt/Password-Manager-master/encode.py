from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

# pwd = "Hu5ky"

password = None
try:
    password = open(".pwd", "r").read()
except IOError:
    pass


# Generate RSA keys， save these keys to files
if password is None:  # Haven't used yet, get new keys and save
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    with open("private.pem", "wb") as f:
        f.write(private_key)
    with open("public.pem", "wb") as f:
        f.write(public_key)


# RSA
def encode(message):
    with open("public.pem", "rb") as f:
        public_key = f.read()

    rsa_key = RSA.import_key(public_key)

    rsa_cipher = PKCS1_OAEP.new(rsa_key)
    encrypted_message = rsa_cipher.encrypt(message.encode())  # to byte
    # to string, to unicode
    return base64.urlsafe_b64encode(encrypted_message).decode()


def decode(encrypted_message):
    # Load the private key
    with open("private.pem", "rb") as f:
        private_key = f.read()

    rsa_key = RSA.import_key(private_key)
    rsa_cipher = PKCS1_OAEP.new(rsa_key)

    # Decode the Base64 encoded encrypted message
    decoded_encrypted_message = base64.urlsafe_b64decode(
        encrypted_message.encode())

    # Decrypt the message
    decrypted_message = rsa_cipher.decrypt(decoded_encrypted_message)
    return decrypted_message.decode()
