""" A command class for data imports. """

from clrtools.commands.commands_impl import AbstrCommand


class CommandImport(AbstrCommand):
    """ Import data into the DWH. """

    kwargs_opts = {
        "target": (
            "-t",
            "--target",
            dict(
                default="generic",
                type=str,
                required=True,
                help="Defines the target for the import.",
            ),
        ),
        "quarter": (
            "-q",
            "--quarter",
            dict(
                default="generic",
                type=int,
                required=True,
                help="Sets the year/quarter for the import, e.g. 20183.",
            ),
        ),
        "force": (
            "-f",
            "--force",
            dict(
                default=False,
                action="store_true",
                help="Replace data that is already there.",
            ),
        ),
    }

    positional_help = {
        "file": "Path to the file to be imported.",
    }


    def __init__(self, spec):
        self.spec = spec

    def __call__(self, file, target=None, quarter=0, force=False):
        
        print("Import attempt for target", target, "quarter", quarter,
             "from file", file)
        print("force is", force)


