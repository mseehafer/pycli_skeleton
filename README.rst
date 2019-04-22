

CLI Skeleton
================


This skeleton provides a base structure for a pip-installable
command line application.

It is inpired by the *alemic* package (https://github.com/sqlalchemy/alembic)
and the tutorial found at https://python-packaging.readthedocs.io/en/latest/minimal.html.


The entry point is the main function in the config submodule.

The project can be installed in editable mode with *pip install -e .*.

New classes for task of the command line tool can be added by subclassing
as given class.

