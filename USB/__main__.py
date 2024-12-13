from session import Session
import sys,os
"""
couche 4: Application
"""
def main():
    ROOT = os.path.realpath(sys.argv[0])
    print(ROOT)
    session = Session(ROOT)
    try:
        session.start()
    except KeyboardInterrupt:
        print("Process forced to stop")
    
if __name__ == '__main__':
    main()