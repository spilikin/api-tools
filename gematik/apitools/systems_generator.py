import click
import requests
import csv

@click.command()
def systems_generator():
    print("Generating systems")
    csvdata = csv.DictReader(requests.get("https://raw.githubusercontent.com/kitameg/Produktmodell/main/Insight/Produkttyp.csv").text.split("\n"),
      dialect="excel")

    for row in csvdata:
      print(row)