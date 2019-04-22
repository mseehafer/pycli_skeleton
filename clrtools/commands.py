""" The commands for the CLI app. Each function 
    in this module creates a command with the same
    name, positional arguments become positional parameters,
    default arguments become optional paramters.
"""


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


class CommandGetImportTargets(AbstrCommand):
    """ Display the available target for a data import
    """

    kwargs_opts = None

    positional_help = None

    def __init__(self, spec):
        self.spec = spec

    def __call__(self):
        targets = ["GDWHCoA", "ECONCoA", "QuasiiSingle", "YieldCurve"]

        for tar in targets:
            print(tar)


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
    }

    positional_help = {
        "file": "Path to the file to be imported.",
    }


    def __init__(self, spec):
        self.spec = spec

    def __call__(self, file, target=None, quarter=0):
        
        print("Import attempt for target", target, "quarter", quarter,
             "from file", file)




def import_targets(config):
    """Display the available target for a data import

    :param config: a :class:`.Config` object.

    """

    targets = ["GDWHCoA", "ECONCoA", "QuasiiSingle", "YieldCurve"]

    for tar in targets:
        print(tar)



def load(config, target, file):
    """List available commands

    :param config: a :class:`.Config` object.

    :param file: the file to be imported

    :param target: type of datat to be loaded, use `targets` to see the list of available target

    """

    print("Available templates:\n")
    print("config =", config)
 




def init(config, directory, template="generic"):
    """Initialize a new scripts directory.

    :param config: a :class:`.Config` object.

    :param directory: string path of the target directory

    :param template: string name of the migration environment template to
     use.

    """
    
    print("init:", directory, template)


def revision(
    config,
    message=None,
    autogenerate=False,
    sql=False,
    head="head",
    splice=False,
    branch_label=None,
    version_path=None,
    rev_id=None,
    depends_on=None,
    process_revision_directives=None,
):
    """Create a new revision file.

    :param config: a :class:`.Config` object.

    :param message: string message to apply to the revision; this is the
     ``-m`` option to ``alembic revision``.

    :param autogenerate: whether or not to autogenerate the script from
     the database; this is the ``--autogenerate`` option to
     ``alembic revision``.

    :param sql: whether to dump the script out as a SQL string; when specified,
     the script is dumped to stdout.  This is the ``--sql`` option to
     ``alembic revision``.

    :param head: head revision to build the new revision upon as a parent;
     this is the ``--head`` option to ``alembic revision``.

    :param splice: whether or not the new revision should be made into a
     new head of its own; is required when the given ``head`` is not itself
     a head.  This is the ``--splice`` option to ``alembic revision``.

    :param branch_label: string label to apply to the branch; this is the
     ``--branch-label`` option to ``alembic revision``.

    :param version_path: string symbol identifying a specific version path
     from the configuration; this is the ``--version-path`` option to
     ``alembic revision``.

    :param rev_id: optional revision identifier to use instead of having
     one generated; this is the ``--rev-id`` option to ``alembic revision``.

    :param depends_on: optional list of "depends on" identifiers; this is the
     ``--depends-on`` option to ``alembic revision``.

    :param process_revision_directives: this is a callable that takes the
     same form as the callable described at
     :paramref:`.EnvironmentContext.configure.process_revision_directives`;
     will be applied to the structure generated by the revision process
     where it can be altered programmatically.   Note that unlike all
     the other parameters, this option is only available via programmatic
     use of :func:`.command.revision`

     .. versionadded:: 0.9.0

    """

    print("revision",
          message,
          autogenerate,
          sql,
          head,
          splice,
          process_revision_directives)


def upgrade(config, revision, sql=False, tag=None):
    """Upgrade to a later version.

    :param config: a :class:`.Config` instance.

    :param revision: string revision target or range for --sql mode

    :param sql: if True, use ``--sql`` mode

    :param tag: an arbitrary "tag" that can be intercepted by custom
     ``env.py`` scripts via the :meth:`.EnvironmentContext.get_tag_argument`
     method.

    """

    print("upgrade:", revision, sql, tag)


def show(config, rev):
    """Show the revision(s) denoted by the given symbol.

    :param config: a :class:`.Config` instance.

    :param revision: string revision target

    """

    print("show", rev)