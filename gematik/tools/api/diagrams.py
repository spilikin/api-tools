import click
from . import systems
from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

@click.command()
def diagrams():
  print("Generating diagrams")
  sm = systems.load_all("src/telematik/systems")
  print(sm.systems)
  
  with Diagram("Web Service", show=True):
    ELB("lb") >> EC2("web") >> RDS("userdb")