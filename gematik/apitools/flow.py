import click
from rich import print
from rich.progress import track
from jinja2 import Environment, PackageLoader, select_autoescape
from .playbook import build_playbook
from .model import Flow, FlowVertexType
import yaml
import csv

@click.command()
def flow():
    env = Environment(
      loader=PackageLoader("gematik", "apitools/templates"),
      autoescape=select_autoescape()
    )
    template = env.get_template("DrawIOFlow.csv")

    playbook = build_playbook()
    
    data = yaml.safe_load(open("src/ti/flow.yaml"))
    flow = Flow(**data)
    flow_name = "Overview"

    fieldnames = ['node','kind','title','connections','url','style']
    rows = list()

    for node in flow.nodes:
      row = {
        "node": node.id(),
        "kind": "",
        "title": node.id(),
        "connections": [],
        "url": None,
        "style": None,
      }

      row['connections'] = ",".join(map(lambda c: c.to, node.connects if node.connects != None else []))

      if node.type() == FlowVertexType.System:        
        row["style"] = "label;whiteSpace=wrap;html=1;image=data:image/png,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;fontStyle=16"
      elif node.type() == FlowVertexType.User:
        row["style"] = "sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#232F3D;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.user;"

      rows.append(row)


    with open(f"src/drawio/{flow_name}.csv", "w") as out:
      out.write(template.render(flow=flow, playbook=playbook))
      out.write('\n')
      writer = csv.DictWriter(out, fieldnames=fieldnames)
      writer.writeheader()
      writer.writerows(rows)

