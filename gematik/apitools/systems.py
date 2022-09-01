from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel, Field
import glob
from .literals import ApprovalType
import yaml

class Meta(BaseModel):
  cn: str
  version: str
  title: Optional[str]
  icon: Optional[str]

class SystemApprovalContextSpec(BaseModel):
  cn: Union[ApprovalType, str]
  version: str

class ProvidedInterfaceSpec(BaseModel):
  name: str
  description: Optional[str]
  version: Optional[str]
  definitionURL: Optional[str]

class RequiredInterfaceSpec(BaseModel):
  name: str
  sourceSystem: Optional[str]
  sourceSystemVersion: Optional[str]
  description: Optional[str]


class SystemComponentSpec(BaseModel):
  name: str
  providedInterfaces: Optional[List[ProvidedInterfaceSpec]]

class SystemStereotype(str, Enum):
  ClientGeneric = "ClientGeneric"
  ServiceGeneric = "ServiceGeneric"
  ClientPractitioner = "ClientPractitioner"
  ClientMobile = "MobileApp"
  TIPlatformService = "TIPlatformService"
  TIEndUserHardware = "TIEndUserHardware"
  TISmartcard = "TISmartcard"
  TIApplicationService = "TIApplicationService"
  TIApplicationClient = "TIApplicationClient"
  TIApplicationClientMobile = "TIApplicationClientApp"
  TIApplicationClientNative = "TIApplicationClientNative"
  TIApplicationClientWeb = "TIApplicationClientWeb"

class SystemSpec(BaseModel):
  stereotype: SystemStereotype
  approvalContext: Optional[SystemApprovalContextSpec]
  components: Optional[List[SystemComponentSpec]]
  providedInterfaces: Optional[List[ProvidedInterfaceSpec]]
  requiredInterfaces: Optional[List[RequiredInterfaceSpec]]

class System(BaseModel):
  """
  Describes any system in context of telematics infrastructure
  """
  apiVersion: str = Field("v1", const=True)
  kind: str = Field("System", const=True)
  meta: Meta
  spec: SystemSpec

class SystemsManager():
  systems: List[System] = list()

def load_all(path: str) -> SystemsManager:
  sm = SystemsManager()
  for file in glob.glob(f"{path}/**/*.yaml", recursive=True):
    data = yaml.safe_load(open(file))
    sm.systems.append(System(**data))
    
  return sm