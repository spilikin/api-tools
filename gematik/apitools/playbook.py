from glob import glob
from typing import List
import yaml
from .model import System

class Playbook():
  systems: List[System] = list()

def build_playbook() -> Playbook:
  playbook = Playbook()
  # find all systems
  for file in glob(f"src/ti/systems/*.yaml", recursive=True):
    data = yaml.safe_load(open(file))
    playbook.systems.append(System(**data))
    
  return playbook