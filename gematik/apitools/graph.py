import click
from rich import print
from rich.progress import track
from .model import System, SystemKind

from igraph import Graph, plot
import matplotlib.pyplot as plt

def add_system(g: Graph, system: System) -> System:
  g.add_vertex(system.canonical, model=system)
  return system

@click.command()
def graph():
  g: Graph = Graph().as_directed()

  InternetServices = add_system(g, System(canonical="internet-services", kind=SystemKind.NetworkInternet))
  InternetAccess = add_system(g, System(canonical="internet-access", kind=SystemKind.NetworkInternet))
  vpn_service = add_system(g, System(canonical="vpn-service", kind=SystemKind.TIPlatformService))
  ti_network = add_system(g, System(canonical="ti-network", kind=SystemKind.TIPlatformService))

  eprescription_service = add_system(g, System(canonical="eprescription-service", kind=SystemKind.TIApplicationService))
  eprescription_frontend = add_system(g, System(canonical="eprescription-frontend", kind=SystemKind.TIApplicationClientMobile))

  directory = add_system(g, System(canonical="directory", kind=SystemKind.TIPlatformService))

  idp_service = add_system(g, System(canonical="idp-service", kind=SystemKind.TIPlatformService))

  connector = add_system(g, System(canonical="connector", kind=SystemKind.TIUserHardware))

  card_terminal = add_system(g, System(canonical="card-terminal", kind=SystemKind.TIUserHardware))

  mobile_card_terminal = add_system(g, System(canonical="mobile-card-terminal", kind=SystemKind.TIUserHardware))

  ehc = add_system(g, System(canonical="electronic-health-card", kind=SystemKind.TISmartcard))
  hpc = add_system(g, System(canonical="health-professional-card", kind=SystemKind.TISmartcard))

  pharmacies_directory = add_system(g, System(canonical="pharmacies-directory", kind=SystemKind.TIPlatformService))

  basis_consumer = add_system(g, System(canonical="basis-consumer", kind=SystemKind.TIPlatformService))

  kim_client_module = add_system(g, System(canonical="kim-client-module", kind=SystemKind.TIApplicationClient))
  email_client = add_system(g, System(canonical="email-client", kind=SystemKind.ClientGeneric))

  health_professional_software = add_system(g, System(canonical="health-professional-software", kind=SystemKind.ClientPractitioner))
  
  ehr_personal_frontend = add_system(g, System(canonical="ehr-personal-frontend", kind=SystemKind.TIApplicationClient))

  eprescription_privacy_frontend = add_system(g, System(canonical="eprescription-privacy-frontend", kind=SystemKind.TIApplicationClient))

  kim_service = add_system(g, System(canonical="kim-service", kind=SystemKind.TIApplicationService))

  gematik_root_ca = add_system(g, System(canonical="gematik-root-ca", kind=SystemKind.TIPlatformService))

  idp_federated = add_system(g, System(canonical="idp-federated", kind=SystemKind.TIPlatformService))
  idp_federation_master = add_system(g, System(canonical="idp-federation-master", kind=SystemKind.TIPlatformService))

  vsdm_intermediary = add_system(g, System(canonical="vsdm-intermediary", kind=SystemKind.TIApplicationService))
  vsdm_vsd = add_system(g, System(canonical="vsdm-vsd", kind=SystemKind.TIApplicationService))
  vsdm_ufs = add_system(g, System(canonical="vsdm-ufs", kind=SystemKind.TIApplicationService))
  vsdm_cms = add_system(g, System(canonical="vsdm-cms", kind=SystemKind.TIApplicationService))
  
  connector_highspeed = add_system(g, System(canonical="connector-highspeed", kind=SystemKind.TIPlatformService))

  HealthInsurancePrivacyFrontend = add_system(g, System(canonical="HealthInsurancePrivacyFrontend", kind=SystemKind.TIApplicationClient))
  HealthInsuranceConsumer = add_system(g, System(canonical="HealthInsuranceConsumer", kind=SystemKind.TIPlatformService))

  NCPeH = add_system(g, System(canonical="NCPeH", kind=SystemKind.TIPlatformService))

  OCSPProxy = add_system(g, System(canonical="OCPProxy", kind=SystemKind.TIPlatformService))

  PrivateKeyGenerator = add_system(g, System(canonical="PrivateKeyGenerator", kind=SystemKind.TIPlatformService))

  GatewayExistingNetworks = add_system(g, System(canonical="GatewayExistingNetworks", kind=SystemKind.TIPlatformService))
  EHRKeyGenerationService = add_system(g, System(canonical="EHRKeyGenerationService", kind=SystemKind.TIApplicationService))
  AuthnSignatureService = add_system(g, System(canonical="AuthnSignatureService", kind=SystemKind.TIPlatformService))

  SMBC = add_system(g, System(canonical="SMCB", kind=SystemKind.TISmartcard))

  TIMessengerClient = add_system(g, System(canonical="TIMessengerClient", kind=SystemKind.TIApplicationService))
  TIMessengerService = add_system(g, System(canonical="TIMessengerClient", kind=SystemKind.TIApplicationService))

  g.add_edge(connector.canonical, InternetAccess.canonical)
  g.add_edge(InternetAccess.canonical, vpn_service.canonical)
  
  g.add_edge(card_terminal.canonical, connector.canonical)
  g.add_edge(ehc.canonical, card_terminal.canonical)
  g.add_edge(hpc.canonical, card_terminal.canonical)

  g.add_edge(vpn_service.canonical, ti_network.canonical)

  g.add_edge(ti_network.canonical, eprescription_service.canonical)

  g.add_edge(eprescription_frontend.canonical, InternetServices.canonical)
  
  g.add_edge(ti_network.canonical, directory.canonical)

  g.add_edge(pharmacies_directory.canonical, directory.canonical)

  g.add_edge(ti_network.canonical, idp_service.canonical)

  g.add_edge(ehc.canonical, mobile_card_terminal.canonical)
  g.add_edge(hpc.canonical, mobile_card_terminal.canonical)

  g.add_edge(InternetServices.canonical, eprescription_service.canonical)
  g.add_edge(InternetServices.canonical, directory.canonical)
  g.add_edge(InternetServices.canonical, pharmacies_directory.canonical)
  g.add_edge(InternetServices.canonical, idp_service.canonical)

  g.add_edge(basis_consumer.canonical, ti_network.canonical)

  g.add_edge(kim_client_module.canonical, connector.canonical)
  g.add_edge(email_client.canonical,kim_client_module.canonical)

  g.add_edge(health_professional_software.canonical,kim_client_module.canonical)
  g.add_edge(health_professional_software.canonical,connector.canonical)

  g.add_edge(ehr_personal_frontend.canonical, InternetServices.canonical)
  g.add_edge(eprescription_privacy_frontend.canonical, InternetServices.canonical)

  g.add_edge(ti_network.canonical, kim_service.canonical)

  g.add_edge(ti_network.canonical, gematik_root_ca.canonical)
  g.add_edge(InternetServices.canonical, gematik_root_ca.canonical)

  g.add_edge(InternetServices.canonical, idp_federated.canonical)
  g.add_edge(InternetServices.canonical, idp_federation_master.canonical)
  g.add_edge(idp_federated.canonical, idp_federation_master.canonical)

  g.add_edge(ti_network.canonical, vsdm_intermediary.canonical)
  g.add_edge(vsdm_intermediary.canonical, vsdm_ufs.canonical)
  g.add_edge(vsdm_intermediary.canonical, vsdm_cms.canonical)
  g.add_edge(vsdm_intermediary.canonical, vsdm_vsd.canonical)

  g.add_edge(card_terminal.canonical, connector_highspeed.canonical)
  g.add_edge(connector_highspeed.canonical, InternetAccess.canonical)

  g.add_edge(HealthInsuranceConsumer.canonical, ti_network.canonical)
  g.add_edge(HealthInsurancePrivacyFrontend.canonical, InternetServices.canonical)

  g.add_edge(ti_network.canonical, NCPeH.canonical)

  g.add_edge(ti_network.canonical, OCSPProxy.canonical)

  g.add_edge(InternetServices.canonical, PrivateKeyGenerator.canonical)

  g.vs["label"] = g.vs["name"]

  print(g.vs["label"])



  layout = g.layout("tree")
  plot(g, layout=layout, bbox=(0,0,1900,1000))
  
  #fig, ax = plt.subplots()
  #plot(g, layout=layout, target=ax, vertex_label=g.vs["label"])
  #plt.show()
  