



class CommandError(Exception):
    """ General error class for scripts."""
    pass


class AbstrCommand(object):

    kwargs_opts = None

    positional_help = None

    def __init__(self, spec):
        self.spec = spec

    def __call__(self):
        pass
