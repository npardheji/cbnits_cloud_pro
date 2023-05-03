import adal
import os
import requests
import json 

def azure_msdefender_storage_enable():
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
    "properties": {
        "pricingTier": "Standard",
        "subPlan": "PerStorageAccount"
    }
    }
    payload=json.dumps(payload)

    url=f'https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.Security/pricings/StorageAccounts?api-version=2022-03-01'
    response = requests.request("PUT", url, headers=headers, data = payload)
    
    return response.text







def azure_msdefender_app_service_enable():
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
    "properties": {
        "pricingTier": "Standard" 
    }
    }
    payload=json.dumps(payload)

    url=f'https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.Security/pricings/AppServices?api-version=2022-03-01'
    response = requests.request("PUT", url, headers=headers, data = payload)
    
    return response.text


def azure_msdefender_ContainerRegistry_enable():
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
    "properties": {
        "pricingTier": "Standard" 
    }
    }
    payload=json.dumps(payload)

    url=f'https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.Security/pricings/ContainerRegistry?api-version=2022-03-01'
    response = requests.request("PUT", url, headers=headers, data = payload)
    
    return response.text


def azure_msdefender_KeyVaults_enable():
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
    "properties": {
        "pricingTier": "Standard" 
    }
    }
    payload=json.dumps(payload)

    url=f'https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.Security/pricings/KeyVaults?api-version=2022-03-01'
    response = requests.request("PUT", url, headers=headers, data = payload)
    
    return response.text


def azure_msdefender_SqlServerVirtualMachines_enable():
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
    "properties": {
        "pricingTier": "Standard" 
    }
    }
    payload=json.dumps(payload)

    url=f'https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.Security/pricings/SqlServerVirtualMachines?api-version=2022-03-01'
    response = requests.request("PUT", url, headers=headers, data = payload)
    
    return response.text


