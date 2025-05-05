from message import Message

from UserInterface import *
from keyholder import *

GenNewKeys("./home/trino", b"test")
keyh = KeyHolder("./home/trino", b"test")




user = User("trino", b"test", "./home/trino", 1)
MSG = Message(user)
MSG.loadData("Hello World!")
trame = MSG.getTrame()
print()

MSG = None
MSG = Message(user)
MSG.read(trame, user.keyholder.public)
print(MSG.getResponse())