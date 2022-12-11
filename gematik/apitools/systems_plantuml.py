import click
from rich import print
from rich.progress import track
from jinja2 import Environment, PackageLoader, select_autoescape
import os

@click.command()
def systems_plantuml():
    print("Generating systems")

    env = Environment(
      loader=PackageLoader("gematik", "apitools/templates"),
      autoescape=select_autoescape()
    )

    template = env.get_template("System.puml")

    sm = load_all(".")

    os.makedirs("src/plantuml/systems", exist_ok = True)

    for system in track(sm.systems, description="Creating PlantUML files..."):
      with open(f"src/plantuml/systems/{system.meta.cn}.puml", "w") as out:
        out.write(template.render(system=system))
