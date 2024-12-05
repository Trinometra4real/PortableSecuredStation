class UserStorage:
    def __init__(self, datapack:str):
        new = open(datapack, "rb")
        self.content = list(bytearray(new.read()))
        new.close()
        

        if folder != None:
            for element in folder:
                getdict = parcourir(element)
                self.tree.update(getdict)              


        if file != None:
            for element in file:
                getdict = parcourir(element)
                self.tree.update(getdict)
    class File:
