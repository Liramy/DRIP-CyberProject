from cryptography.fernet import Fernet
import json
from os import path

class Kdot:
    def __init__(self):
        """Define an object for encrypting and decrypting objects using the
           json format.

        Args:
            key (bytes): The key saved in order to encrypt and decrypt
        """
        if not path.exists("chat-key.key"):
            self.key = Fernet.generate_key()
            if not path.exists("chat-key.key"):
                with open("chat-key.key", "wb") as key_file:
                    key_file.write(self.key)
        else:
            self.key = open("chat-key.key", "rb").read()
        
        self.cipher_suite = Fernet(self.key)
        
    
    def encrypt_obj(self, obj):
        """Function for encrypting an object

        Args:
            obj (any): An object that you wish to transfer in sockets

        Returns:
            bytes: transferable string encrypted
        """
        serialized_obj = json.dumps(obj).encode()
        encrypted_obj = self.cipher_suite.encrypt(serialized_obj)
        return encrypted_obj
    
    def decrypt_obj(self, enc):
        """Function for decrypting an object

        Args:
            enc (bytes): Encrypted byte of an object

        Returns:
            any: Decrypted object
        """
        decrypted_obj = self.cipher_suite.decrypt(enc)
        deserialized_obj = json.loads(decrypted_obj.decode())
        return deserialized_obj
