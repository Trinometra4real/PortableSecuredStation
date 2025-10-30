import os, sys


    
class DiskManagerNtfs:
    PARTITION_0 = [235, 82, 144, 78, 84, 70, 83, 32, 32, 32, 32, 0, 2, 8, 0, 0, 0, 0, 0, 0, 0, 248, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 128, 0, 128, 0, 255, 15, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 255, 0, 0, 0, 0, 0, 0, 0, 246, 0, 0, 0, 1, 0, 0, 0, 166, 4, 115, 51, 205, 60, 231, 100, 0, 0, 0, 0, 14, 31, 190, 113, 124, 172, 34, 192, 116, 11, 86, 180, 14, 187, 7, 0, 205, 16, 94, 235, 240, 50, 228, 205, 22, 205, 25, 235, 254, 84, 104, 105, 115, 32, 105, 115, 32, 110, 111, 116, 32, 97, 32, 98, 111, 111, 116, 97, 98, 108, 101, 32, 100, 105, 115, 107, 46, 32, 80, 108, 101, 97, 115, 101, 32, 105, 110, 115, 101, 114, 116, 32, 97, 32, 98, 111, 111, 116, 97, 98, 108, 101, 32, 102, 108, 111, 112, 112, 121, 32, 97, 110, 100, 13, 10, 112, 114, 101, 115, 115, 32, 97, 110, 121, 32, 107, 101, 121, 32, 116, 111, 32, 116, 114, 121, 32, 97, 103, 97, 105, 110, 32, 46, 46, 46, 32, 13, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 85, 170]
    
    
    def __init__(self, disk_image_path: str):
        self.disk_image_path = disk_image_path
        with open(self.disk_image_path, "rb") as f:
            self.size = f.read(-1).__len__()
        self.max_sector = self.size // 512
        dizaine=0
        while (self.size>2**(dizaine*10)):
            dizaine+=1
        units = ["B", "KB", "MB", "GB", "TB", "PB"]
        print("loaded disk of size: ", self.size/2**(10*(dizaine-1)), units[dizaine-1])

    def format(self):
        with open(self.disk_image_path, "wb") as f:
            f.seek(0)
            f.write(bytearray(self.PARTITION_0))
            f.seek((self.max_sector-1)*512)
            
    def read_sector(self, sector:int) -> bytes:
        with open(self.disk_image_path, "rb") as f:
            print("reading sector : ", sector,"->",sector+1, "/", self.max_sector)
            f.seek(512*sector)
            return f.read(512)
        
        
        
        
data = DiskManagerNtfs("./storage_disk.iso").read_sector(int(sys.argv[1]))
if data == b"":
    print("Sector out of buffer size")
    sys.exit(0)

num = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
buffer = []
final_table = []
for i in range(data.__len__()):
    if i % 32 == 0 and i != 0:
        final_table.append(buffer)
        buffer = []
        buffer.append(data[i])
    else:
        buffer.append(data[i])
final_table.append(buffer)


for i in range(0, final_table.__len__()):
    print(num[i] ," - " , final_table[i])
    
    