import adal
import os
import requests
import json

def flowlog(resourceGroupName, nsg, storage,retention_day,netwatcher):

    """{
    "cloud": "azure",
    "policy_type": "Network",
    "policy": "azure_nsg_flow_log_custom_enforcement",
    "custom_env": {
        "resourceGroupName": "cloud-custodian",
        "nsg_name": "Ni3-NSG",
        "storage": "newstoragens",
        "retention_day": 100,
        "netwatcher": "NetworkWatcher_centralindia"
        }
    
    }"""

    subscription_id = os.environ.get('AZURE_SUBSCRIPTION_ID')
    client_id=os.environ.get('AZURE_CLIENT_ID')
    client_secret=os.environ.get('AZURE_CLIENT_SECRET')
    tenant_id=os.environ.get('AZURE_TENANT_ID')

    authority_url = 'https://login.microsoftonline.com/'+tenant_id
    context = adal.AuthenticationContext(authority_url)
    token = context.acquire_token_with_client_credentials(
        resource='https://management.azure.com/',
        client_id=client_id,
        client_secret=client_secret
    )

    accesstoken = token["accessToken"]
    headers={'Authorization': 'Bearer ' + accesstoken,
                'Content-Type': 'application/json'}


    payload={
          'targetResourceId': f'/subscriptions/{subscription_id}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/networkSecurityGroups/{nsg}',
          'properties': {
          'storageId': f'/subscriptions/{subscription_id}/resourceGroups/{resourceGroupName}/providers/Microsoft.Storage/storageAccounts/{storage}',
          'enabled': 'true',
          'retentionPolicy' : {
                'days': f'{retention_day}',
                'enabled': True
              },
          'format': {
              'type': 'JSON',
              'version': 2
          }
        }
      }


    payload=json.dumps(payload)
    
    url=f'https://management.azure.com/subscriptions/{subscription_id}/ResourceGroups/NetworkWatcherRG/providers/Microsoft.Network/networkWatchers/{netwatcher}/configureFlowLog?api-version=2016-12-01'

    response = requests.request("POST", url, headers=headers, data = payload)
    
    return response.text