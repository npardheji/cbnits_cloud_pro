import os
import random
from azure.identity import DefaultAzureCredential
from azure.mgmt.network._network_management_client import NetworkManagementClient
from azure.mgmt.network.v2020_04_01.models import NetworkSecurityGroup, SecurityRule


def nsg_security_rule(resourceGroupName, nsg_name, source_address_prefix, direction, access, protocol,destination_port_range, destination_address_prefix, source_port_range):

  """{
    "cloud": "azure",
    "policy_type": "Network",
    "policy": "flowlog",
    "custom_env": {
        "resourceGroupName": "cloud-custodian",
        "nsg_name": "Ni3-NSG",
        "protocols": "UDP",
        "source_add": "0.0.0.0/0",
        "access": "Deny",
        "dport": "445"
        }
  }"""

  subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
  credentials = DefaultAzureCredential()

  network_client = NetworkManagementClient(
    credentials,
    subscription_id
  )

  network_client.security_rules.begin_create_or_update(resourceGroupName,nsg_name,f"Rule_{random.randint(101,999)}",SecurityRule(
        protocol=protocol,
        destination_address_prefix=destination_address_prefix,
        access=access,
        direction=direction,
        description='my_rules',
        source_port_range=source_port_range,
        destination_port_range=destination_port_range,
        source_address_prefix=source_address_prefix,
        #destination_port_ranges=["1000","1005","2005","2020"],
        priority=random.randint(101,999),
        name=f"my_{random.randint(101,999)}"))
  return "**complete**"


def nsg_security_rule_allow(resourceGroupName, nsg_name, protocols,source_add,dport):

  """{
    "cloud": "azure",
    "policy_type": "Network",
    "policy": "flowlog",
    "custom_env": {
        "resourceGroupName": "cloud-custodian",
        "nsg_name": "Ni3-NSG",
        "protocols": "UDP",
        "source_add": "0.0.0.0/0",
        "access": "Deny",
        "dport": "445"
        }
  }"""

  subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
  credentials = DefaultAzureCredential()

  network_client = NetworkManagementClient(
    credentials,
    subscription_id
  )

  network_client.security_rules.begin_create_or_update(resourceGroupName,nsg_name,f"Rule_{random.randint(101,999)}",SecurityRule(
        protocol=protocols,
        #source_address_prefix='*',
        destination_address_prefix='*',
        access="Allow",
        direction='Inbound', description='my_rules',source_port_range='*',
        destination_port_range=dport,
        source_address_prefix=source_add,
        #destination_port_ranges=["1000","1005","2005","2020"],
        priority=random.randint(101,999), name=f"my_{random.randint(101,999)}"))
  return "**complete**"