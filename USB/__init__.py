# rsaencrypt/.__init__.py
from keyholder import *
from session import Session
from __main__ import *
from infos import *
from keyholder import *
import logging

__all__ = ["main", "Session", "helpCommand"]
"""
Couche 0: Storage
Couche 1: Encryption
Couche 2: Session
Couche 4: Application
"""

logging.basicConfig(
    level = logging.DEBUG,
    filename="./rsaencrypt.log"
)

logger = logging.getLogger(__name__)
logger.info("Started the package")

if __name__ == "__main__":
    main()