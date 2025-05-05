import tkinter as TK
import os, sys
from session import Session
def main():
    ROOT = __file__.replace("/App/__main__.py", "")
    print("Welcome to Arsenal Builder !")
    
    cmd = Session(ROOT)
    cmd.start()
    
    print("Session exited")

if __name__ == "__main__":
    main()