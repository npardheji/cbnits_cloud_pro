import  os
import adal
import json
import requests
import random

def resource_group_lock(resourceGroupName):

    '''{
    "cloud": "azure",
    "policy_type": "Network",
    "policy": "subnet",
    "custom_env": {
        "resourceGroupName": "cloud-custodian",
        }
    
    }'''

    subscription_id = os.environ.get('AZURE_SUBSCRIPTION_ID')
    client_id = os.environ.get('AZURE_CLIENT_ID')
    client_secret = os.environ.get('AZURE_CLIENT_SECRET')
    tenant_id = os.environ.get('AZURE_TENANT_ID')

    authority_url = 'https://login.microsoftonline.com/' + tenant_id
    context = adal.AuthenticationContext(authority_url)
    token = context.acquire_token_with_client_credentials(
        resource='https://management.azure.com/',
        client_id=client_id,
        client_secret=client_secret
    )

    accesstoken = token["accessToken"]
    headers = {'Authorization': 'Bearer ' + accesstoken,
               'Content-Type': 'application/json'}

    payload = {
        "properties": {
            "level": "ReadOnly"
        }
    }

    payload = json.dumps(payload)

    # url=f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/cloud-custodian/providers/Microsoft.Web/sites/chikentanduri/basicPublishingCredentialsPolicies/ftp?api-version=2022-03-01'
    url = f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resourceGroupName}/providers/Microsoft.Authorization/locks/testlock_{random.randint(1,100000):05}?api-version=2016-09-01'

    response = requests.request("PUT", url, headers=headers, data=payload)

    return "...................done..............." + response.text