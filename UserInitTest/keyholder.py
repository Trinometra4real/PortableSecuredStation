from math import dist
from Crypto.PublicKey import RSA as rsa
from Crypto.Cipher import PKCS1_OAEP
import getpass, base64, hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
__all__ = ["KeyHolder"]
"""
Couche 1: Encryption
"""

class KeyHolder:
    
    def __init__(self, home, passphrase:bytes):
        self.home = home
        try:
            print(home+"/private.key")
            new = open(home+"/private.key", "rb")
            
            self.encrowprivate = new.read()
            new.close()
            new = open(home+"/public.crt", "rb")
            self.encrowpublic = new.read()
            new.close()
            self.passphrase = passphrase
            
            
        except FileNotFoundError:
            print('No cipher key found, fatal error')
            exit(0)
        

    def newKeys(self):
        keys = rsa.generate(bits=2048)
        self.private = rsa.import_key(keys.exportKey())
        self.public = rsa.import_key(keys.public_key().export_key())
        
    
    def close(self):
        self.poluteKey()
        with open(self.home+"/public.crt", "wb") as f:
            f.write(self.encrowpublic)
        with open(self.home+"/private.key", "wb") as f:
            f.write(self.encrowprivate)
        return True
    

    def poluteKey(self):
        
        aes= AES.new(self.passphrase, AES.MODE_ECB)
        self.encrowprivate=base64.b64encode(aes.encrypt(pad(self.private.exportKey(), 32)))
        self.encrowpublic=base64.b64encode(aes.encrypt(pad(self.public.exportKey(), 32)))
        

    def purifyKey(self, passphrase) -> bool:
        aes = AES.new(passphrase, AES.MODE_ECB)
        
        self.decrowprivate = unpad(aes.decrypt(base64.b64decode(self.encrowprivate)), 32)
        self.decrowpublic = unpad(aes.decrypt(base64.b64decode(self.encrowpublic)), 32)
        
        patternpub = "-----BEGIN PUBLIC KEY-----"
        patternpub = patternpub.encode("utf-8")
        patternpriv = "-----BEGIN RSA PRIVATE KEY-----"
        patternpriv = patternpriv.encode("utf-8")

        if self.decrowpublic[0:patternpub.__len__()] == patternpub and self.decrowprivate[0:patternpriv.__len__()] == patternpriv:
            
            self.public = rsa.importKey(self.decrowpublic)
            self.private = rsa.importKey(self.decrowprivate)
            self.deccipher = PKCS1_OAEP.new(self.private)
            self.enccipher = PKCS1_OAEP.new(self.public)
            return True
        else:
            return False
    
    def signMessage(self, msg:bytes)-> str:
        hash =hashlib.sha256(msg).digest()
        finalbuffer=pow(int.from_bytes(hash, byteorder="big"), self.private.d, self.private.n).to_bytes(length=256, byteorder="big")
        return base64.b64encode(finalbuffer).decode("utf-8")
        

    def encrypt(self, buffer:bytes)-> bytes:
        finalbuffer = b''
        rest = buffer.__len__()%190
        phase_num = int((buffer.__len__()-rest)/190)
        for i in range(0,phase_num):
            finalbuffer+= self.enccipher.encrypt(buffer[i*190:(i+1)*190])
        finalbuffer+=self.enccipher.encrypt(buffer[phase_num*190:phase_num*190+rest])
        return finalbuffer
 
    def decrypt(self, buffer:bytes)-> bytes:
        plainbuffer = b''
        if (buffer.__len__()%256!=0):
            return b''
        else:
            for i in range(0, buffer.__len__()//256):
                plainbuffer+=self.deccipher.decrypt(buffer[i*256:(i+1)*256])
        return plainbuffer
    
    def verify(self, msg:bytes, b64Sign:str)-> bool:
        hash = hashlib.sha256(msg).digest()
        Signature = base64.b64decode(b64Sign.encode("utf-8"))
        CryptoHash = pow(int.from_bytes(Signature, "big"), self.public.e, self.public.n).to_bytes(length=32, byteorder="big")
        if (hash == CryptoHash):

            return True
        else:
            return False
            
def GenNewKeys(path, passphrase:bytes):
    keys = rsa.generate(bits=2048)
    
    pub = keys.public_key().export_key()
    priv = keys.exportKey()
    
    
    aes  = AES.new(passphrase, AES.MODE_ECB)
    pub = base64.b64encode(aes.encrypt(pad(pub, 32)))
    priv= base64.b64encode(aes.encrypt(pad(priv, 32)))
    

    new = open(path+"/private.key", "wb")
    new.write(priv)
    new.close()
    new = open(path+"/public.crt", "wb")
    new.write(pub)
    new.close()

def checkDifferences(A:list, B:list)-> None:
        coordinates = []
        if (A.__len__() != B.__len__()):
            if A.__len__()> B.__len__():
                maxlen = B.__len__()
            else:
                maxlen = A.__len__()
        else:
            maxlen = A.__len__()
        for i in range(0, maxlen):
            if A[i] != B[i]:
                coordinates.append([A[i], B[i]])
