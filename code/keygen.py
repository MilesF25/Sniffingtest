from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature


""" This file is for encryption and loading keys to a file. It makes exchanging keys easier. Will probably be added later"""


# I plan to implement encryption, the code is all here but i just need to acutally implement it


def generate_key_pair():
    key_size = 2048

    private_key = rsa.generate_private_key(
        public_exponent=65537,  # Do not change
        key_size=key_size,
    )

    public_key = private_key.public_key()
    return private_key, public_key


def save_keys_to_file(private_key, public_key, filename="key_file.txt"):
    # Convert private key to PEM format (human-readable),
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    # Convert public key to PEM format (human-readable)
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    # Save both keys to file with clear separation
    with open(filename, "wb") as f:
        f.write(private_pem)
        f.write(b"\n")
        f.write(public_pem)

    print(f"Keys successfully written to {filename}")


def load_keys_from_file(filename="key_file.txt"):
    with open(filename, "rb") as f:
        file_content = f.read()

    # Find the separator between keys =
    private_end = file_content.find(b"-----END PRIVATE KEY-----") + len(
        b"-----END PRIVATE KEY-----"
    )

    # Split the content
    private_pem = file_content[:private_end]
    public_pem = file_content[private_end:].strip()

    # Load keys from PEM format
    private_key = serialization.load_pem_private_key(private_pem, password=None)

    public_key = serialization.load_pem_public_key(public_pem)

    return private_key, public_key


def encrypt(message, public_key):
    return public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def decrypt(message_encrypted, private_key):
    try:
        message_decrypted = private_key.decrypt(
            message_encrypted,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return f"Decrypted Message: {message_decrypted}"
    except ValueError:
        return "Failed to Decrypt"
