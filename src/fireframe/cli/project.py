import click
import os
from pathlib import Path


@click.group()
@click.pass_context
def project_cli(ctx):
    ctx.ensure_object(dict)


@project_cli.command()
@click.argument("name", required=True, type=str)
@click.option("--path", "-p", type=click.Path())
@click.pass_context
def create(ctx, name: str, path):
    click.echo(f"Creating new project {name}...")
    # create a new subdirectory to path if given,
    # otherwise create a new subdirectory to current working directory
    # with the name of the project
    if path:
        Path(path).mkdir(parents=True, exist_ok=True)
        os.mkdir(os.path.join(path, name))
    elif not os.path.exists(name):
        os.makedirs(os.path.join(os.getcwd(), name))


@project_cli.command()
@click.argument("name", required=True, type=str)
@click.pass_context
def startapp(ctx, name: str):
    click.echo(f"Starting new app {name}...")
    raise NotImplementedError("Implement project startapp.")
