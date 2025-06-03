from math import dist
import rsa
import getpass, base64
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
        self.public, self.private = rsa.newkeys(nbits=2048)
    
    def close(self):
        self.poluteKey()
        with open(self.home+"/public.crt", "wb") as f:
            f.write(self.encrowpublic)
        with open(self.home+"/private.key", "wb") as f:
            f.write(self.encrowprivate)
        return True
    

    def poluteKey(self):
        
        aes= AES.new(self.passphrase, AES.MODE_ECB)
        self.encrowprivate=base64.b64encode(aes.encrypt(pad(self.private.save_pkcs1(), 32)))
        self.encrowpublic=base64.b64encode(aes.encrypt(pad(self.public.save_pkcs1(), 32)))
        

    def purifyKey(self, passphrase) -> bool:
        aes = AES.new(passphrase, AES.MODE_ECB)
        
        self.decrowprivate = unpad(aes.decrypt(base64.b64decode(self.encrowprivate)), 32)
        self.decrowpublic = unpad(aes.decrypt(base64.b64decode(self.encrowpublic)), 32)
        
        patternpub = "-----BEGIN RSA PUBLIC KEY-----"
        patternpub = patternpub.encode("utf-8")
        patternpriv = "-----BEGIN RSA PRIVATE KEY-----"
        patternpriv = patternpriv.encode("utf-8")
        
        if list(bytearray(self.decrowpublic))[0:patternpub.__len__()] == list(bytearray(patternpub)) and list(bytearray(self.decrowprivate))[0:patternpriv.__len__()] == list(bytearray(patternpriv)):
            self.public = rsa.PublicKey.load_pkcs1(self.decrowpublic)
            self.private = rsa.PrivateKey.load_pkcs1(self.decrowprivate)
            return True
        else:
            return False
    
    def signMessage(self, msg:bytes)-> bytes:
        signed = rsa.sign(msg, self.private, "sha256")
        return signed

    def encrypt(self, msg:bytes)-> bytes:
        buffer = list(bytearray(msg))
        
        result = b''
        while True:
            if buffer.__len__()%245!=0:
                buffer.append(0)
            else:
                break
        i=0
        print(buffer)
        print("___________END BUFFER____________")
        
        while i<buffer.__len__():
            row = rsa.encrypt(bytes(bytearray(buffer[i:i+244])), self.public)
            print("buffer: ", buffer[i:i+244].__len__())
            print("row crypted: ", row.__len__())
            result+=row
            print(row)
            
            i+=245
        
        print("__________________END RESULT___________________")
        
        return result
    
    def decrypt(self, encrypted:bytes)-> bytes:
        i=0
        result=[]
        while i<encrypted.__len__():
            cryptorow = bytes(bytearray(list(bytearray(encrypted))[i:i+255]))
            row = rsa.decrypt(cryptorow, self.private)
            result.extend(list(bytearray(row)))
            i+=256
        while True:
            if (result[-1]==0):
                del result[-1]
            else:
                break
        return bytearray(bytes(result))
    
    def verify(self, msg:bytes, Signature:bytes, distPub:rsa.PublicKey)-> str:
        return rsa.verify(msg, Signature, distPub)


    
            
def GenNewKeys(path, passphrase:bytes):
    pub, priv = rsa.newkeys(nbits=2048)
    
    pub = pub.save_pkcs1()
    priv = priv.save_pkcs1()
    
    
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
