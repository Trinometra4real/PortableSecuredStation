from math import dist
import rsa
import getpass
__all__ = ["KeyHolder"]
"""
Couche 1: Encryption
"""

class KeyHolder:
    def __init__(self, home, passphrase:bytes):
        print(list(bytearray(passphrase)))
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
        self.public, self.private = rsa.newkeys(nbits=4096)
    
    def close(self):
        self.poluteKey()
        with open(self.home+"/public.crt", "wb") as f:
            f.write(self.rowpublic)
        with open(self.home+"/private.key", "wb") as f:
            f.write(self.rowprivate)
        return True
    

    def poluteKey(self):
        self.rowpublic = list(bytearray(self.public.save_pkcs1()))
        self.rowprivate = list(bytearray(self.private.save_pkcs1()))
        self.passphrase = list(bytearray(self.passphrase))

        for i in range(0, self.rowpublic.__len__()):
            self.rowpublic[i] = (self.rowpublic[i]-self.passphrase[i%self.passphrase.__len__()])%256
        for i in range(0, self.rowprivate.__len__()):
            self.rowprivate[i] = (self.rowprivate[i]-self.passphrase[i%self.passphrase.__len__()])%256

    def purifyKey(self, passphrase) -> bool:
        self.rowpublic = list(bytearray(self.rowpublic))
        self.rowprivate = list(bytearray(self.rowprivate))
        passphrase = list(bytearray(passphrase))
        for i in range(0, self.rowpublic.__len__()):
            self.rowpublic[i] = (self.rowpublic[i]+passphrase[i%passphrase.__len__()])%256
        for i in range(0, self.rowprivate.__len__()):
            self.rowprivate[i] = (self.rowprivate[i]+passphrase[i%passphrase.__len__()])%256
        
        patternpub = "-----BEGIN RSA PUBLIC KEY-----"
        patternpub = list(bytearray(patternpub.encode("utf-8")))
        patternpriv = "-----BEGIN RSA PRIVATE KEY-----"
        patternpriv = list(bytearray(patternpriv.encode("utf-8")))
        
        if self.rowpublic[0:patternpub.__len__()] == patternpub and self.rowprivate[0:patternpriv.__len__()] == patternpriv:
            self.public = rsa.PublicKey.load_pkcs1(bytes(bytearray(self.rowpublic)))
            self.private = rsa.PrivateKey.load_pkcs1(bytes(bytearray(self.rowprivate)))
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
            
def GenNewKeys(path, passphrase):
    pub, priv = rsa.newkeys(nbits=4096)
    
    pub = pub.save_pkcs1()
    priv = priv.save_pkcs1()
    
    public = list(bytearray(pub))
    private = list(bytearray(priv))
    passphrase = list(bytearray(passphrase))

    for i in range(0, public.__len__()):
        public[i] = (public[i]-passphrase[i%passphrase.__len__()])%256
    for i in range(0, private.__len__()):
        private[i] = (private[i]-passphrase[i%passphrase.__len__()])%256

    pub = bytes(bytearray(public))
    priv = bytes(bytearray(private))

    new = open(path+"/private.key", "wb")
    new.write(priv)
    new.close()
    new = open(path+"/public.crt", "wb")
    new.write(pub)
    new.close()

if __name__ == '__main__':
    main()