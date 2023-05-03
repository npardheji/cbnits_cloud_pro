import adal
import os
import requests
import json 

def azure_soft_delete(resourceGroupName, retentiondays,storage_account_name):
    subscription_id = os.environ.get('AZURE_SUBSCRIPTION_ID')
    RESOURCE_GROUP_NAME=resourceGroupName
    ACCOUNT_NAME=storage_account_name
    retentiondays=retentiondays
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

    payload=  { 
        "properties": { 
        "deleteRetentionPolicy": { 
        "enabled": True, 
        "days": "{}".format(retentiondays), 
        "allowPermanentDelete": True 
        }} 
    }

    payload=json.dumps(payload)

    url=f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{RESOURCE_GROUP_NAME}/providers/Microsoft.Storage/storageAccounts/{ACCOUNT_NAME}/blobServices/default?api-version=2022-09-01'
    response = requests.request("PUT", url, headers=headers, data = payload)

    return response.text