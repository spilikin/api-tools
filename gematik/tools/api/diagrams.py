import click
from . import systems
from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.onprem.client import Client, User
from diagrams.onprem.compute import Server
from diagrams.generic.compute import Rack
from diagrams.custom import Custom
from diagrams.generic.network import Firewall, Switch

@click.command()
def diagrams():
  print("Generating diagrams")
  sm = systems.load_all("src/telematik/systems")


  with Diagram("TI Network", show=True):
    user = User("Practitioner")
    with Cluster("Office"):
      pvs = Client("PVS")
      with Cluster("TI"):
        kon = Server("Konnektor")
        kt = Server("eHealth-KT")
        egk = Server("eGK")
    kt >> kon
    egk >> kt
    user >> kt
    user >> pvs
    pvs >> kon
    with Cluster("Zugang"):
      vpnzd = Firewall("VPN-ZD")
      szzp1 = Switch("SZZP")
      vpnzd >> szzp1
    with Cluster("TI Platform"):
      tsps = [
        Server("tsp1"),
        Server("tsp2"),
        Server("tsp3"),
        Server("tsp4"),
        Server("tsp5"),
      ]
      szzp2 = Switch("SZZP")
    szzp1 >> tsps
    tsps >> szzp2
    kon >> vpnzd
    with Cluster("Apps"):
      app_group = [
        Server("app1"),
        Server("app2"),
        Server("app3"),
        Server("app4"),
      ]
    internet = Switch("Internet")
    szzp2 >> app_group
    app_group >> internet
    user2 = User("aaa")
    user2 << internet
