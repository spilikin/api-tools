import click

from gematik.tools.api.systems_generator import systems_generator
from . import systems
from .diagrams import diagrams

@click.command()
def schema():
  print("Schemas")
  open("schema/System.schema.json", "w").write(systems.System.schema_json(indent=2))

@click.group()
def cli():
    pass

cli.add_command(schema)
cli.add_command(diagrams)
cli.add_command(systems_generator)
  