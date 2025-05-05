from UserInterface import User
import json
import rsa
import base64
import datetime
#             user: clear ASCII
#             date: clear ASCII
#             data: encodedBase64
#             sign: encodedBase64


class Message:
    def __init__(self, user:str):
        self.user = user
        new = open(__file__.replace("message.py", "model.json"), "r")
        
        self.trame = json.loads(new.read())
        new.close()
        self.response=""

    def loadData(self, data:bytes, pubkey:rsa.PublicKey=None, encoded=False):
        if encoded:
            data=base64.b64encode(rsa.encrypt(data.encode(), pubkey)).decode()
            self.trame["encrypted"]="TRUE"
            
        else:
            self.trame["data"] = base64.b64encode(data.encode()).decode()
            self.trame["encrypted"]="FALSE"
            
        
        self.trame["user"]=self.user.user
        self.trame["sign"] = ""
        self.trame["date"] = str(datetime.datetime.now())
        signature = self.user.keyholder.signMessage(json.dumps(self.trame).encode())

        
        self.trame["sign"] = base64.b64encode(signature).decode()
        
        self.rowtrame = json.dumps(self.trame)
        print(self.trame)

    def getTrame(self):
        return self.rowtrame
    

    def read(self, rowtrame:str, pubkey:rsa.PublicKey=None)-> bool:
        trame = json.loads(rowtrame)
        print(trame)
        signature  = base64.b64decode(trame["sign"].encode())
        trame["sign"] = ""

        if pubkey!=None:
            try:
                rsa.verify(json.dumps(trame).encode(), signature, pubkey)

            except rsa.VerificationError:
                print("Verification Failed")
                return False
            
        if trame["encrypted"]=="TRUE":
            self.response= self.user.keyholder.decrypt(base64.b64decode(trame["data"])).decode()
        
        self.response = base64.b64decode(trame["data"]).decode()

        return True
    

    def getResponse(self):
        return self.response
        


