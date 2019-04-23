""" The commands for the CLI app. Each class in this module 
    inheriting from AbstrCommand
    represents a command with the same
    name. Positional arguments of the :meth:`__call__()`
    become positional parameters,
    default arguments become optional paramters.
"""


from .commands_impl import CommandError
from .commands_impl import AbstrCommand


#from clrtools.commands.commands_impl import CommandError
#from clrtools.commands.commands_impl import AbstrCommand

# import command classes here
#from clrtools.commands.commands_impl.load import CommandImport
#from clrtools.commands.commands_impl.targets import CommandShowTargets

from .commands_impl.load import CommandImport
from .commands_impl.targets import CommandShowImportTargets
