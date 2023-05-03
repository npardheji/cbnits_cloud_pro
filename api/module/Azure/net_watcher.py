from azure.identity import DefaultAzureCredential
from azure.mgmt.network._network_management_client import NetworkManagementClient
import os


def network_watcher():
    subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
    credentials = DefaultAzureCredential()
    network_client = NetworkManagementClient(credentials, subscription_id)
    network_watcher_list = network_client.network_watchers.list_all()
    count=0

    output= []
    for network_watcher in network_watcher_list:
      output.append(str(network_watcher))
      #print(n)
      count=count+1
    return output,"count : {}".format(count)
    #print(count) 