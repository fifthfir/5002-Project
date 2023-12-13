import base64

ori_key = "Hu5ky"

password = None
try:
    password = open(".pwd", "r").read()
except IOError:
    pass


# A encoding similar to Vigenere cipher
# https://gist.github.com/ilogik/6f9431e4588015ecb194

def vigenere_encode(text):
    encoded_chars = []

    for i, char in enumerate(text):
        key_char = ori_key[i % len(ori_key)]
        # Get the corresponding key character
        encoded_char = chr((ord(char) + ord(key_char)) % 256)
        encoded_chars.append(encoded_char)

    encoded_text = "".join(encoded_chars)
    return base64.urlsafe_b64encode(encoded_text.encode('utf8'))


def vigenere_decode(encoded_text):
    decoded_chars = []

    # Decode Base64 and convert to utf-8
    decoded_text = base64.urlsafe_b64decode(encoded_text).decode("utf8")

    for i, char in enumerate(decoded_text):
        # Get the corresponding key character
        key_char = ori_key[i % len(ori_key)]
        decoded_char = chr((ord(char) - ord(key_char)) % 256)
        decoded_chars.append(decoded_char)

    decoded_text = "".join(decoded_chars)
    return decoded_text
