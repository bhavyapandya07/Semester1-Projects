from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import os

# Generate RSA keys for both tiers if not exist
def generate_rsa_keys():
    if not os.path.exists("private_public.pem") or not os.path.exists("public_public.pem"):
        key_public = RSA.generate(2048)
        with open("private_public.pem", "wb") as f:
            f.write(key_public.export_key())
        with open("public_public.pem", "wb") as f:
            f.write(key_public.publickey().export_key())
        print("Public tier RSA keys generated.")
    else:
        print("Public tier keys already exist, skipping.")

    if not os.path.exists("private_private.pem") or not os.path.exists("public_private.pem"):
        key_private = RSA.generate(2048)
        with open("private_private.pem", "wb") as f:
            f.write(key_private.export_key())
        with open("public_private.pem", "wb") as f:
            f.write(key_private.publickey().export_key())
        print("Private tier RSA keys generated.")
    else:
        print("Private tier keys already exist, skipping.")

# Encrypt file using chosen tier's public key
def encrypt_file(input_file_path, output_file_path, tier_public_key_path):
    try:
        recipient_key = RSA.import_key(open(tier_public_key_path, "rb").read())
        session_key = get_random_bytes(16)  # AES key

        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        enc_session_key = cipher_rsa.encrypt(session_key)

        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        with open(input_file_path, "rb") as infile:
            plaintext = infile.read()
        ciphertext, tag = cipher_aes.encrypt_and_digest(plaintext)

        with open(output_file_path, "wb") as out_file:
            out_file.write(len(enc_session_key).to_bytes(2, byteorder='big'))
            out_file.write(enc_session_key)
            out_file.write(cipher_aes.nonce)
            out_file.write(tag)
            out_file.write(ciphertext)

        print(f"File '{input_file_path}' encrypted for {tier_public_key_path} and saved as '{output_file_path}'.")
    except Exception as e:
        print(f"Encryption failed: {e}")

# Decrypt file using chosen tier's private key
def decrypt_file(enc_file_path, output_file_path, tier_private_key_path):
    try:
        private_key = RSA.import_key(open(tier_private_key_path, "rb").read())
        with open(enc_file_path, "rb") as f:
            len_enc_key = int.from_bytes(f.read(2), byteorder='big')
            enc_session_key = f.read(len_enc_key)
            nonce = f.read(16)
            tag = f.read(16)
            ciphertext = f.read()

        cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key = cipher_rsa.decrypt(enc_session_key)

        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)

        with open(output_file_path, "wb") as out_file:
            out_file.write(data)

        print(f"File '{enc_file_path}' decrypted and saved as '{output_file_path}'.")
    except Exception as e:
        print(f"Decryption failed: {e}")

# CLI Menu
def main():
    generate_rsa_keys()
    print("\nSecure File Storage with Tier Selection")
    print("Select Tier:")
    print("1. Public Tier")
    print("2. Private Tier")
    tier_choice = input("Enter your tier choice: ")

    if tier_choice == "1":
        pub_key = "public_public.pem"
        priv_key = "private_public.pem"
        tier_name = "Public Tier"
    elif tier_choice == "2":
        pub_key = "public_private.pem"
        priv_key = "private_private.pem"
        tier_name = "Private Tier"
    else:
        print("Invalid tier choice.")
        return

    print(f"\nSelected Tier: {tier_name}")
    print("1. Encrypt and Upload File")
    print("2. Decrypt and Download File")
    action_choice = input("Enter your choice: ")

    if action_choice == "1":
        file_in = input("Enter path of file to encrypt: ")
        file_out = input("Enter output encrypted file path: ")
        encrypt_file(file_in, file_out, pub_key)
    elif action_choice == "2":
        enc_file = input("Enter path of encrypted file: ")
        restored_file = input("Enter path for decrypted output: ")
        decrypt_file(enc_file, restored_file, priv_key)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()