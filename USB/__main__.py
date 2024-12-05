from session import Session
import sys,os
"""
couche 4: Application
"""
def main():
    ROOT = os.path.realpath(sys.argv[1])
    print(ROOT)
    session = Session(ROOT +"USB/scripts/python/rsaencrypt")
    session.start()
    
if __name__ == '__main__':
    main()