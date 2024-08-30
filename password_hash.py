from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class Hash:
    secret_password = "738881f14ead291d25de0b782f920558"
    def pass_encrypt(self,password):
       salt = get_random_bytes(16)
       Key = PBKDF2(self.secret_password, salt, dkLen=32)
       password = bytes(password, 'utf-8')
       cipher = AES.new(Key, AES.MODE_CBC)
       ciphered_data = cipher.encrypt(pad(password, AES.block_size))
       final_password_hash = salt+cipher.iv+ciphered_data
       
       return final_password_hash
           
    def pass_decrypt(self,encrypted_pass):
        salt=encrypted_pass[:16]
        iv = encrypted_pass[16:32]
        decrypt_data = encrypted_pass[32:] 
        Key = PBKDF2(self.secret_password, salt, dkLen=32)
        cipher = AES.new(Key, AES.MODE_CBC, iv=iv)
        original = unpad(cipher.decrypt(decrypt_data), AES.block_size).decode('utf-8')
        
        return original