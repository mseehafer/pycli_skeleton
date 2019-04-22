""" Configuration object and main entry point for the CLI application. """

import os
from argparse import ArgumentParser
from configparser import ConfigParser
import inspect
import collections

from . import commands


# taken from alembic.utils.compat
ArgSpec = collections.namedtuple(
    "ArgSpec", ["args", "varargs", "keywords", "defaults"]
)

def inspect_getargspec(func):
    return ArgSpec(*inspect.getfullargspec(func)[0:4])


class Config(object):

    """Represent a configuration.
    :param file_: name of the .ini file to open.
    :param ini_section: name of the main section within the
     .ini file which is used

    :param config_args: A dictionary of keys and values that will be used
     for substitution in the alembic config file.  The dictionary as given
     is **copied** to a new one, stored locally as the attribute
     ``.config_args``. When the :attr:`.Config.file_config` attribute is
     first invoked, the replacement variable ``here`` will be added to this
     dictionary before the dictionary is passed to ``ConfigParser()``
     to parse the .ini file.
    """

    def __init__(
        self,
        file_=None,
        ini_section="clrtools",
        cmd_opts=None,
        config_args=dict(),
    ):
        """Construct a new :class:`.Config`
        """
        self.config_file_name = file_
        self.config_ini_section = ini_section
        self.cmd_opts = cmd_opts
        self.config_args = dict(config_args)

        if self.config_file_name:
            here = os.path.abspath(os.path.dirname(self.config_file_name))
        else:
            here = ""
        self.config_args["here"] = here
        file_config = ConfigParser(self.config_args)
        if self.config_file_name:
            file_config.read([self.config_file_name])
        else:
            file_config.add_section(self.config_ini_section)
        
        self.file_config = file_config


    cmd_opts = None
    """The command-line options passed to the ``alembic`` script.
    """

    config_file_name = None
    """Filesystem path to the .ini file in use."""

    config_ini_section = None
    """Name of the config file section to read basic configuration
    from.  Defaults to ``clrtools``, that is the ``[clrtools]`` section
    of the .ini file.  This value is modified using the ``-n/--name``
    option to the CLI runnier.
    """

    def get_section(self, name):
        """Return all the configuration options from a given .ini file section
        as a dictionary.
        """
        return dict(self.file_config.items(name))

    def get_section_option(self, section, name, default=None):
        """Return an option from the given section of the .ini file.
        """
        if not self.file_config.has_section(section):
            raise util.CommandError(
                "No config file %r found, or file has no "
                "'[%s]' section" % (self.config_file_name, section)
            )
        if self.file_config.has_option(section, name):
            return self.file_config.get(section, name)
        else:
            return default

    def get_main_option(self, name, default=None):
        """Return an option from the 'main' section of the .ini file.
        This defaults to being a key from the ``[alembic]``
        section, unless the ``-n/--name`` flag were used to
        indicate a different section.
        """
        return self.get_section_option(self.config_ini_section, name, default)


class CommandLine(object):
    def __init__(self, prog=None):
        self._generate_args(prog)

    def _generate_args(self, prog):

        def add_options2(parser, positional, kwargs, cls):

            for arg in kwargs:
                assert arg in cls.kwargs_opts.keys(), f"Missing spec for option {arg}"
                args = cls.kwargs_opts[arg]
                args, kw = args[0:-1], args[-1]
                parser.add_argument(*args, **kw)

            for arg in positional:
                assert arg in cls.positional_help.keys(), f"Missing spec for arg {arg}"
                #subparser.add_argument(arg, help=positional_help.get(arg))
                parser.add_argument(arg, help=cls.positional_help.get(arg))


        parser = ArgumentParser(prog=prog)
        parser.add_argument(
            "-c",
            "--config",
            type=str,
            default="clrtools.ini",
            help="Alternate config file",
        )
        parser.add_argument(
            "-n",
            "--name",
            type=str,
            default="data-warehouse",
            help="Name of section in .ini file to " "use for the config",
        )

        subparsers = parser.add_subparsers()

        # Loop through all command classes (i.e. those that inherit from AbstrCommand)
        # from the :module': commands.
        for fn_cls in [getattr(commands, n) for n in dir(commands)]:
            if (
                inspect.isclass(fn_cls)
                and fn_cls.__name__[0] != "_"
                and fn_cls.__name__ != "AbstrCommand"
                and issubclass(fn_cls, commands.AbstrCommand)
            ):

                spec = inspect_getargspec(fn_cls.__call__)
                if spec[3]:  # map defaults if any
                    positional = spec[0][1 : -len(spec[3])]
                    kwarg = spec[0][-len(spec[3]) :]
                else:
                    positional = spec[0][1:]
                    kwarg = []

                def _transform_command_name(name):
                    """ Generate the option name starting from the
                        class name, remove the "Command" at the beginning
                        and split at the capital letters (the CamelCase)
                        by "-" (and using only lower case otherwise)
                    """

                    assert len(name) > 7, "Command class name bust have at least length 8"
                    assert name[:7] == "Command", "Command class must start with 'Command' " +\
                                                  "but doesn't: {}".format(name)
                    assert name[7].isupper, "Command class name is supposed to be in CamelCase " +\
                                            " but isn't: {}".format(name)
                    
                    core_name = name[len("Command"):]
                    cap_letter_ind = [i for i, c in enumerate(core_name) if c.isupper()]
                    cap_letter_ind.append(len(core_name))
                
                    substrs = [core_name[cap_letter_ind[j]:cap_letter_ind[j+1]].lower() for j in range(len(cap_letter_ind)-1)]
                    return "-".join(substrs)
                
                cmd_name = _transform_command_name(fn_cls.__name__)
                
                subparser = subparsers.add_parser(cmd_name, help=fn_cls.__doc__)
                add_options2(subparser, positional, kwarg, fn_cls)
                subparser.set_defaults(cmd=(fn_cls, positional, kwarg))
        self.parser = parser

    def run_cmd(self, config, options):
        fn, positional, kwarg = options.cmd

        try:
            # create the command object
            fn_inst = fn(config)

            # run the __call__ method
            fn_inst(
                # config,
                *[getattr(options, k, None) for k in positional],
                **dict((k, getattr(options, k, None)) for k in kwarg)
            )
        except commands.CommandError as e:
            if options.raiseerr:
                raise
            else:
                util.err(str(e))

    def main(self, argv=None):
        options = self.parser.parse_args(argv)
        if not hasattr(options, "cmd"):
            # see http://bugs.python.org/issue9253, argparse
            # behavior changed incompatibly in py3.3
            self.parser.error("too few arguments")
        else:
            cfg = Config(
                file_=options.config,
                ini_section=options.name,
                cmd_opts=options,
            )
            self.run_cmd(cfg, options)


def main(argv=None, prog=None, **kwargs):
    """The console runner function for ClrTools."""

    CommandLine(prog=prog).main(argv=argv)


def joke():
    return "Hello!3"

