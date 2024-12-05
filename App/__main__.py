import tkinter as TK
import os

def main():
    a = input("USB path: ")
    if not decrypt(a):
        print("Decrypt failed")

    os.system("python.exe "+a)
    
    

def decrypt(path):
    return True

if __name__ == "__main__":
    main()