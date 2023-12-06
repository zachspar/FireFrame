import os
from pathlib import Path

import click


@click.group()
@click.pass_context
def project_cli(ctx):
    ctx.ensure_object(dict)


@project_cli.command()
@click.argument("name", required=True, type=str)
@click.option("--path", "-p", type=click.Path())
@click.pass_context
def create(ctx, name: str, path):
    """
    Create a new FireFrame project scaffold.
    """
    click.echo(f"Creating new project {name}...")
    # create a new subdirectory to path if given,
    # otherwise create a new subdirectory to current working directory
    # with the name of the project
    if path:
        Path(path).mkdir(parents=True, exist_ok=True)
        os.mkdir(os.path.join(path, name))
    elif not os.path.exists(name):
        os.makedirs(os.path.join(os.getcwd(), name))

    # NOTE: We should probably use proper templates for these files
    # create a file called main.py in the new project directory
    with open(os.path.join(os.getcwd(), name, "main.py"), "w") as f:
        f.write(f"# Path: {name}/main.py\n\n")
        f.write(f"from fireframe.core.api import FireFrameAPI\n")
        f.write(f"from fireframe.core.viewsets import crud_viewset\n\n")
        f.write(f"from serializers import Example{name.capitalize()}Serializer\n")
        f.write(f"from views import Example{name.capitalize()}ListAPIView\n\n")
        f.write(f'app = FireFrameAPI(name="{name}", version="0.0.0")\n\n')
        f.write(f"# TODO: Add your routes here\n")
        f.write(f"app.include_router(crud_viewset(Example{name.capitalize()}Serializer))\n")
        f.write(f"app.include_router(Example{name.capitalize()}ListAPIView())\n")

    # create a file called models.py in the new project directory
    with open(os.path.join(os.getcwd(), name, "models.py"), "w") as f:
        f.write(f"# Path: {name}/models.py\n\n")
        f.write(f"from fireframe.core.models import Model\n\n")
        f.write(f"class Example{name.capitalize()}Model(Model):\n")
        f.write(f"    example: str\n\n")
        f.write(f"# TODO: Add more models here\n")

    # create a file called serializers.py in the new project directory
    with open(os.path.join(os.getcwd(), name, "serializers.py"), "w") as f:
        f.write(f"# Path: {name}/serializers.py\n\n")
        f.write("from fireframe.core.serializers import ModelSerializer\n\n")
        f.write(f"from models import Example{name.capitalize()}Model\n\n")
        f.write(f"class Example{name.capitalize()}Serializer(ModelSerializer):\n")
        f.write(f"    class Meta:\n")
        f.write(f"        model = Example{name.capitalize()}Model\n")
        f.write(f'        fields = ["example"]\n\n')
        f.write(f"# TODO: Add more serializers here\n")

    # create a file called views.py in the new project directory
    with open(os.path.join(os.getcwd(), name, "views.py"), "w") as f:
        f.write(f"# Path: {name}/views.py\n\n")
        f.write("from fireframe.core.views import BaseListAPIView\n\n")
        f.write(f"from serializers import Example{name.capitalize()}Serializer\n\n")
        f.write(f"class Example{name.capitalize()}ListAPIView(BaseListAPIView):\n")
        f.write(f"    serializer_class = Example{name.capitalize()}Serializer\n\n")
        f.write(f"# TODO: Add more views here\n")


@project_cli.command()
@click.option("--port", "-p", type=int, default=8000)
@click.pass_context
def serve(ctx, port: int):
    """
    Run the FireFrame project.
    """
    click.echo(f"Running FireFrame project on port {port}  ...")
    # check if uvicorn is installed via pip
    try:
        import uvicorn
    except ImportError:
        click.echo("Uvicorn is not installed. Installing it via pip.")
        os.system("pip install uvicorn")

    # check if the project has a main.py file
    if not os.path.exists(os.path.join(os.getcwd(), "main.py")):
        click.echo("No main.py file found. Please run this command from the root directory of your project.")
        return

    # run the project with uvicorn in background
    os.system(f"uvicorn main:app --reload --port {port} --host '0.0.0.0'")
