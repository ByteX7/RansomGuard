#This script will only work if the victim has the decryption key ⚠️

import os
import base64
import hashlib
from Crypto.Cipher import AES

class RansomwareAntidote:
    def __init__(self, key):
        self.key = key

    def decrypt_file(self, encrypted_filename):
        try:
            with open(encrypted_filename, 'rb') as encrypted_file:
                # Read the file size
                file_size = int.from_bytes(encrypted_file.read(8), byteorder='big')
                # Read the initialization vector
                iv = encrypted_file.read(16)
                # Create AES decryption object
                decryptor = AES.new(self.key.encode(), AES.MODE_CBC, iv)
                # Decrypt and write to a new file
                with open(encrypted_filename[:-10], 'wb') as decrypted_file:  # Removing '.encrypted' extension
                    while True:
                        chunk = encrypted_file.read(64 * 1024)
                        if len(chunk) == 0:
                            break
                        decrypted_file.write(decryptor.decrypt(chunk))
                    # Truncate the decrypted file to original size
                    decrypted_file.truncate(file_size)
            # Remove the encrypted file after decryption
            os.remove(encrypted_filename)
            print(f"File {encrypted_filename} decrypted successfully.")
        except Exception as e:
            print(f"Error decrypting file {encrypted_filename}: {e}")

# Example usage
def main():
    # Provide the known decryption key
    decryption_key = input("Enter the decryption key: ")

    # Initialize the RansomwareAntidote with the decryption key
    antidote = RansomwareAntidote(decryption_key)

    # Decrypt encrypted files
    encrypted_files = [filename for filename in os.listdir() if filename.endswith('.encrypted')]
    for encrypted_file in encrypted_files:
        antidote.decrypt_file(encrypted_file)

if __name__ == "__main__":
    main()
