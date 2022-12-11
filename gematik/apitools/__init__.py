import click

from .systems_asciidoc import systems_asciidoc
from .systems_plantuml import systems_plantuml
from .graph import graph
from .flow import flow
from . import model
from .diagrams import diagrams
import gettext
from rich import *

_ = gettext.gettext

@click.command()
def schema():
  print(_("Generate schema files"))
  open("schema/System.schema.json", "w").write(model.System.schema_json(indent=2))
  open("schema/Flow.schema.json", "w").write(model.Flow.schema_json(indent=2))

@click.group()
def cli():
    pass

cli.add_command(schema)
cli.add_command(diagrams)
cli.add_command(systems_asciidoc)
cli.add_command(systems_plantuml)
cli.add_command(graph)
cli.add_command(flow)