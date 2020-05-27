from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

class Rsa:
    def __init__(self,public_key=None,private_key=None,key_bits=4096):
        if not public_key and not private_key:
            new_key = RSA.generate(key_bits,e=65537)

            self.private_key = new_key.exportKey('DER')
            self.public_key = new_key.publickey().exportKey('DER')

            self.private = new_key
            self.public = new_key.publickey()

            self.encryptor = PKCS1_OAEP.new(self.public)
            self.decryptor = PKCS1_OAEP.new(self.private)
        else:
            if public_key and private_key:
                self.private = RSA.import_key(private_key)
                self.public = RSA.import_key(public_key)
                self.encryptor = PKCS1_OAEP.new(self.public)
                self.decryptor = PKCS1_OAEP.new(self.private)
            elif public_key:
                self.public = RSA.import_key(public_key)
                self.encryptor = PKCS1_OAEP.new(self.public)

    def encrypt(self,text):
        if self.public:
            if len(text) <= 4096:
                return self.encryptor.encrypt(text.encode('utf8'))
            else:
                data = ''
                data += self.encryptor.encrypt(text[:4096].encode('utf8'))
                data += self.encryptor.encrypt(text[4096:].encode('utf8'))

                return data
        else:
            return False

    def decrypt(self,text):
        if self.private:
            if len(text) <= 4096:
                return self.decryptor.decrypt(text).decode()
            else:
                data = ''
                data += self.decryptor.decrypt(text[:4096]).decode()
                data += self.decryptor.decrypt(text[4096:]).decode()

                # if len(text[4096:]) > 4096:
                #     data += self.decryptor.decrypt(text[8192:]).decode()
                return data
        else:
            return False
