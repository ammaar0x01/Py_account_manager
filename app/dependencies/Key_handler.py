import os 
from cryptography.fernet import Fernet 

# rename to 
# class Kryptic():  
class Key_handler():
    def __init__(self): 
        self._key:bytes 
        self._fernet:Fernet
        self._check_key()
        self._retrieve_key()
    # -----------------------------------  
      
    def _check_key(self) -> None:
        if "e_key.key" not in os.listdir():
            # generate symmetric-encryption key if file doesn't exist
            # print("generating key...")
            key = Fernet.generate_key()
            # print(key)

            # saving key to .key file
            with open("e_key.key", "wb") as e_key:
                e_key.write(key)
                
            # hiding the .key file
            os.system("attrib +h e_key.key")

    def _retrieve_key(self) -> None: 
        with open("e_key.key", "rb") as encrypt:
            self._key = encrypt.read()
            self._fernet = Fernet(self._key)
            
    def encrypt(self, message:str) -> bytes: 
        encrypted = self._fernet.encrypt(message.encode())
        return encrypted

    def decrypt(self, message_bytes:bytes) -> str: 
        decrypted = self._fernet.decrypt(message_bytes).decode() 
        return decrypted
        
# ======================================        
# testing

# obj = Key_handler()
        
# # en = obj.encrypt("the_name_is_hidden")
# # print(en)
# # print()

# # de = obj.decrypt(en)
# # print(de)

# d1 = obj.decrypt(b'gAAAAABnHqfVUZFSRfHJUFZRLl4lsQUUbxT1O36JwFH70vgvhudKUUDBTH7T6Z8csgyy5gM95cDHHL_j4z_-jMui4EjKXjq5uUPhn4S3HOSppM-ZtSkpewk=')
# print(d1)
   
# ======================================        
