""" A command class for showing targets. """

from . import AbstrCommand


class CommandShowImportTargets(AbstrCommand):
    """ Display the available target for a data import
    """

    kwargs_opts = None

    positional_help = None

    def __init__(self, config):
        self.config = config

    def __call__(self):
        targets = ["GDWHCoA", "ECONCoA", "QuasiiSingle", "YieldCurve", "inflation"]

        for tar in targets:
            print(tar)

        # print("Config-Info:")
        # print(self.config.get_main_option("database"))

