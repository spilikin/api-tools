from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel

from .system_literals import SystemCanonical
from .literals import ApprovalType

class ApprovalContext(BaseModel):
  canonical: Union[ApprovalType, str]
  version: str

class ProvidedInterface(BaseModel):
  name: str
  description: Optional[str]
  version: Optional[str]
  definitionURL: Optional[str]

class RequiredInterface(BaseModel):
  name: str
  sourceSystem: Optional[str]
  sourceSystemVersion: Optional[str]
  description: Optional[str]

class SystemComponent(BaseModel):
  name: str
  providedInterfaces: Optional[List[ProvidedInterface]] = list()

class SystemKind(str, Enum):
  NetworkGeneric = "NetworkLAN"
  NetworkInternet = "NetworkInternet"
  ClientGeneric = "ClientGeneric"
  ServiceGeneric = "ServiceGeneric"
  ClientPractitioner = "ClientPractitioner"
  ClientMobile = "MobileApp"
  TINetwork = "TINetwork"
  TIPlatformService = "TIPlatformService"
  TIUserHardware = "TIUserHardware"
  TISmartcard = "TISmartcard"
  TIApplicationService = "TIApplicationService"
  TIApplicationClient = "TIApplicationClient"
  TIApplicationClientMobile = "TIApplicationClientApp"
  TIApplicationClientNative = "TIApplicationClientNative"
  TIApplicationClientWeb = "TIApplicationClientWeb"
  TIPlatformConsumer = "TIPlatformConsumer"

class ProvidedInterfaceInfo(BaseModel):
  systemCanonical: Union[SystemCanonical, str]
  interface: ProvidedInterface
  componentName: Optional[str] = None

class System(BaseModel):
  """
  Describes any system in context of telematics infrastructure
  """
  canonical: Union[SystemCanonical, str]
  kind: Optional[SystemKind]
  version: Optional[str]
  approvalContext: Optional[ApprovalContext]
  components: Optional[List[SystemComponent]] = list()
  providedInterfaces: Optional[List[ProvidedInterface]] = list()
  requiredInterfaces: Optional[List[RequiredInterface]] = list()

  def hasInterfaces(self) -> bool:
    if len(self.providedInterfaces) > 0:
      return True
    
    for c in self.components:
      if len(c.providedInterfaces) > 0:
        return True

  def allProvidedInterfaces(self) -> List[ProvidedInterfaceInfo]:
    result = list()
    for i in self.providedInterfaces:
      result.append(ProvidedInterfaceInfo(systemCanonical=self.canonical, interface=i))

    for c in self.components:
      for i in c.providedInterfaces:
        result.append(ProvidedInterfaceInfo(systemCanonical=self.canonical, interface=i, componentName=c.name))

    return result

class FlowEdge(BaseModel):
  to: Union[SystemCanonical, str]

class FlowVertexType(Enum):
  System = 1
  User = 2
  Operator = 3
  Custom = 4

class FlowVertex(BaseModel):
  system: Optional[SystemCanonical]
  user: Optional[str]
  operator: Optional[str]
  title: Optional[str]
  connects: Optional[List[FlowEdge]]
  style: Optional[str]

  def id(self) -> str:
    type = self.type()
    if type == FlowVertexType.System:
      return f"{self.system}"
    if type == FlowVertexType.User:
      return f"{self.user}"
    if type == FlowVertexType.Operator:
      return f"{self.operator}"
    else:
      return f"{self.title}"

  def type(self) -> FlowVertexType:
    if self.system != None:
      return FlowVertexType.System
    if self.user != None:
      return FlowVertexType.User
    if self.operator != None:
      return FlowVertexType.Operator
    else:
      return FlowVertexType.Custom

class Flow(BaseModel):
  layout: str
  nodes: List[FlowVertex]