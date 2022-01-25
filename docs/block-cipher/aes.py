import hashlib
import base64

from cryptography.fernet import Fernet


def create_url_safe_base64_encoded_bytes(secret):
    """convert secret into 32 url-safe base64-encoded bytes for Fernet key"""
    # get 32 bytes SHA256 hash
    m = hashlib.sha256()
    m.update(secret.encode())
    return base64.urlsafe_b64encode(m.digest())


def encrypt(secret, plain_text):
    f = Fernet(create_url_safe_base64_encoded_bytes(secret))
    return f.encrypt(plain_text.encode()).decode()


def decrypt(secret, cipher):
    f = Fernet(create_url_safe_base64_encoded_bytes(secret))
    return f.decrypt(cipher).decode()


def encrypt_file(input_file_name, output_file_name, secret):
    f = Fernet(create_url_safe_base64_encoded_bytes(secret))
    with open(input_file_name, 'rb') as f_in:
        content_raw = f_in.read()
    encrypted = f.encrypt(content_raw)
    with open(output_file_name, 'wb') as f_out:
        f_out.write(encrypted)

if __name__ == "__main__":
    # cipher_text = encrypt(secret='password', plain_text="message")
    # print(cipher_text)

    # plain_text = decrypt(secret='password', cipher=cipher_text)
    # print(plain_text)


    encrypt_file(input_file_name='index.md', output_file_name='index.md.aes', secret='password')