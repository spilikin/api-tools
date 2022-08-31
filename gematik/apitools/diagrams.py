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
from diagrams.generic.blank import Blank
from diagrams.generic.network import Firewall, Switch

@click.command()
def diagrams():
  print("Generating diagrams")
  sm = systems.load_all("src/telematik/systems")

  graph_attr = {
    "fontsize": "45",
  }

  edge_attr = {
    "arrowhead": "none",
    "arrowtail": "none",
  }

  with Diagram("TI Network", show=True, graph_attr=graph_attr, edge_attr=edge_attr):
    user = User("Practitioner")

    with Cluster("Office"):
      pvs = Client("Software")
      with Cluster("TI Smartcards"):
        egk = Custom("eGK", "./images/icons/smartcard.png")
        hba = Custom("HBA", "./images/icons/smartcard.png")
        smcb = Custom("SMC-B", "./images/icons/smartcard.png")
      with Cluster("TI Hardware"):
        kon = Server("Konnektor")
        kt = Server("eHealth-KT")

    user >> pvs
    pvs >> kon
    [ egk, hba, smcb ] >> kt
    
    with Cluster("Access"):
      vpnzd = Firewall("VPN-ZD")
      szzp1 = Switch("node")
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
