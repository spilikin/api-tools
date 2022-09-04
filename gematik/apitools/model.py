from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel

from .system_literals import SystemCanonical
from .literals import ApprovalType

class SystemApprovalContext(BaseModel):
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
  providedInterfaces: Optional[List[ProvidedInterface]]

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

class System(BaseModel):
  """
  Describes any system in context of telematics infrastructure
  """
  canonical: Union[SystemCanonical, str]
  kind: Optional[SystemKind]
  version: Optional[str]
  approvalContext: Optional[SystemApprovalContext]
  components: Optional[List[SystemComponent]]
  providedInterfaces: Optional[List[ProvidedInterface]]
  requiredInterfaces: Optional[List[RequiredInterface]]

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