""" A command class for showing targets. """


from clrtools.commands.commands_impl import AbstrCommand

class CommandShowTargets(AbstrCommand):
    """ Display the available target for a data import
    """

    kwargs_opts = None

    positional_help = None

    def __init__(self, spec):
        self.spec = spec

    def __call__(self):
        targets = ["GDWHCoA", "ECONCoA", "QuasiiSingle", "YieldCurve", "inflation"]

        for tar in targets:
            print(tar)

