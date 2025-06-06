from Crypto.PublicKey import RSA as rsa
from Crypto.Cipher import PKCS1_OAEP
from random import randint
import hashlib, sys

def encodeSerial(buffer:bytes, cipher:PKCS1_OAEP.PKCS1OAEP_Cipher):
    finalbuffer = b''
    rest = buffer.__len__()%190
    phase_num = int((buffer.__len__()-rest)/190)
    for i in range(0,phase_num):
        finalbuffer+= cipher.encrypt(buffer[i*190:(i+1)*190])
    finalbuffer+=cipher.encrypt(buffer[phase_num*190:phase_num*190+rest])

    return finalbuffer

def decodeSerial(buffer:bytes, cipher:PKCS1_OAEP.PKCS1OAEP_Cipher):
    plainbuffer = b''
    if (buffer.__len__()%256!=0):
        return b''
    else:
        for i in range(0, buffer.__len__()//256):
            plainbuffer+=cipher.decrypt(buffer[i*256:(i+1)*256])
        return plainbuffer




def SignBuffer(msg:bytes, private:rsa.RsaKey):
    hash =hashlib.sha256(msg).digest()

    finalbuffer=pow(int.from_bytes(hash, byteorder="big"), private.d, private.n).to_bytes(length=256, byteorder="big")
    
    
    return finalbuffer


def verifySign(msg:bytes, Signature:bytes, public:rsa.RsaKey):

    hash = hashlib.sha256(msg).digest()
    CryptoHash = pow(int.from_bytes(Signature, "big"), public.e, public.n).to_bytes(length=32, byteorder="big")


    print(CryptoHash, "\n --- \n", hash)
    if (hash == CryptoHash):

        return True
    else:
        return False
    
    

def action():
    keys = rsa.generate(bits=2048)
    encCipher = PKCS1_OAEP.new(keys.public_key())
    decCipher = PKCS1_OAEP.new(keys)
    dico = "abcdefghijklmnopqrstuvwxyz".split()
    row=""
    for i in range(0, 191):
        row +=dico[randint(0, dico.__len__()-1)]
    result = encodeSerial(row.encode("utf-8"), encCipher)
    
    plaintext=decodeSerial(result, decCipher).decode("utf-8")
    if row == plaintext:
        print('decryption success')
        msg = "Try to sign it please"
        Signature = SignBuffer(msg.encode("utf-8"), keys)
        if (verifySign(msg.encode("utf-8"), Signature, keys.public_key())):
            print("Signature verified")
        else:
            print("this is a fake message")

    else:
        print("decryption failed")