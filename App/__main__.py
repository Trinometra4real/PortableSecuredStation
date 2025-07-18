from session import Session
import sys,os
"""
couche 4: Application
"""
def main():
    ROOT = "/usr/lib/PSS"
    print(ROOT)
    session = Session(ROOT)
    try:
        session.start()
    except KeyboardInterrupt:
        session.exit()
        print("Process forced to stop")
    
if __name__ == '__main__':
    main()