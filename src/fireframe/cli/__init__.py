import click

from .project import project_cli


cli = click.CommandCollection(sources=[project_cli])
