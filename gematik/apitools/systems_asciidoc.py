import click
from rich import print
from rich.progress import track
from jinja2 import Environment, PackageLoader, select_autoescape
from .systems import load_all
import os
from urllib.parse import urlparse

def j2_basename(url):
  if url == None:
    return None
  return os.path.basename(url)

def j2_github_url(url):
  parts = urlparse(url)
  if parts.netloc == "raw.githubusercontent.com":
    parts = parts._replace(
      netloc="github.com",
      path=parts.path.replace("/", "/blob/", 3).replace("/blob/", "/", 2)
      )
    return parts.geturl()
  else:
    return url

@click.command()
def systems_asciidoc():
    env = Environment(
      loader=PackageLoader("gematik", "apitools/templates"),
      autoescape=select_autoescape()
    )
    env.filters['basename'] = j2_basename
    env.filters['github_url'] = j2_github_url

    template = env.get_template("System.adoc")

    sm = load_all(".")

    os.makedirs("docs/systems", exist_ok = True)

    for system in track(sm.systems, description="Writing system asciidoc..."):
      with open(f"docs/systems/{system.meta.cn}.adoc", "w") as out:
        out.write(template.render(system=system))
