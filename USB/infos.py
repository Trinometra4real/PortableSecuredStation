#### IMPORTS ####
from Libs import Basics
from Libs import UserInitTest

#### INIT ####
helpCommand = {}

#### BUILDUP ####
helpCommand.update(Basics.infos.helpCommand)
helpCommand.update(UserInitTest.infos.helpCommand)
