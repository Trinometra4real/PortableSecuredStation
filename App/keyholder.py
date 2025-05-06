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
            self.rowprivate = new.read()
            new.close()
            new = open(home+"/public.crt", "rb")
            self.rowpublic = new.read()
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
            f.write(self.rowpublic)
        with open(self.home+"/private.key", "wb") as f:
            f.write(self.rowprivate)
        return True
    

    def poluteKey(self):
        
        aes= AES.new(self.passphrase, AES.MODE_ECB)
        self.rowprivate=aes.encrypt(pad(self.private.save_pkcs1(), AES.block_size))
        self.rowpublic=aes.decrypt(pad(self.public.save_pkcs1(), AES.block_size))
        

    def purifyKey(self, passphrase) -> bool:
        aes = AES.new(passphrase, AES.MODE_ECB)
        self.rowprivate = unpad(aes.decrypt(self.rowprivate), AES.block_size)
        self.rowpublic = unpad(aes.decrypt(self.rowpublic), AES.block_size)
        
        patternpub = "-----BEGIN RSA PUBLIC KEY-----"
        patternpub = patternpub.encode("utf-8")
        patternpriv = "-----BEGIN RSA PRIVATE KEY-----"
        patternpriv = patternpriv.encode("utf-8")
        
        if bytearray(self.rowpublic)[0:patternpub.__len__()] == patternpub and self.rowprivate[0:patternpriv.__len__()] == patternpriv:
            self.public = rsa.PublicKey.load_pkcs1(self.rowpublic)
            self.private = rsa.PrivateKey.load_pkcs1(self.rowprivate)
            return True
        else:
            return False
    
    def signMessage(self, msg:bytes)-> bytes:
        signed = rsa.sign(msg, self.private, "sha256")
        return signed

    def encrypt(self, msg:bytes)-> bytes:
        encrypted = rsa.encrypt(msg, self.public)
        return encrypted
    
    def decrypt(self, encrypted:bytes)-> bytes:
        return rsa.decrypt(encrypted, self.private)
    
    def verify(self, msg:bytes, Signature:bytes, distPub:rsa.key.PublicKey)-> str:
        return rsa.verify(msg, Signature, distPub)


    def checkDifferences(A:list, B:list)-> list:
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
            
def GenNewKeys(path, passphrase:bytes):
    pub, priv = rsa.newkeys(nbits=2048)
    
    pub = pub.save_pkcs1()
    priv = priv.save_pkcs1()
    
    
    aes  = AES.new(passphrase, AES.MODE_ECB)
    pub = aes.encrypt(pad(pub, AES.block_size))
    priv=aes.encrypt(pad(priv, AES.block_size))
    

    new = open(path+"/private.key", "wb")
    new.write(priv)
    new.close()
    new = open(path+"/public.crt", "wb")
    new.write(pub)
    new.close()

if __name__ == '__main__':
    main()