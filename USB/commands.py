#### IMPORT ####
from Libs import Basics
from Libs import UserInitTest

#### INIT ####
command={}

####  BUILDUP ####
command.update(Basics.command.command)
command.update(UserInitTest.command.command)