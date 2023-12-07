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
if password is None:
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    # Save the private key for decryption
    with open("private.pem", "wb") as f:
        f.write(private_key)
    with open("public.pem", "wb") as f:
        f.write(public_key)


# A encoding similar to Vigenere cipher

# def encode(string, key=pwd):
    # encoded_chars = []
    # for i in range(len(string)):
    #     key_c = key[i % len(key)]
    #     # ord() gives the respective ascii value
    #     encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
    #     encoded_chars.append(encoded_c)
    # encoded_string = "".join(encoded_chars)
    # return base64.urlsafe_b64encode(encoded_string.encode('utf8'))


def encode(message):
    with open("private.pem", "rb") as f:
        public_key = f.read()

    rsa_key = RSA.import_key(public_key)

    rsa_cipher = PKCS1_OAEP.new(rsa_key)
    encrypted_message = rsa_cipher.encrypt(message.encode())
    return base64.urlsafe_b64encode(encrypted_message).decode()


# def decode(string, key=pwd):
#     decoded_chars = []
#     # utf-8 to avoid character mapping errors
#     string = base64.urlsafe_b64decode(string).decode("utf8")

#     for i in range(len(string)):
#         key_c = key[i % len(key)]
#         encoded_c = chr(abs(ord(string[i]) - ord(key_c) % 256))
#         decoded_chars.append(encoded_c)
#     decoded_string = "".join(decoded_chars)
#     print(decoded_string)
#     return decoded_string


def decode(encrypted_message):
    # Load the private key
    with open("private.pem", "rb") as f:
        private_key = f.read()

    rsa_key = RSA.import_key(private_key)
    rsa_cipher = PKCS1_OAEP.new(rsa_key)

    # Decode the Base64 encoded encrypted message
    decoded_encrypted_message = base64.urlsafe_b64decode(encrypted_message.encode())

    # Decrypt the message
    decrypted_message = rsa_cipher.decrypt(decoded_encrypted_message)
    return decrypted_message.decode()
