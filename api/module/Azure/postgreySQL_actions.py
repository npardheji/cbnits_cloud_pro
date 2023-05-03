import os
import adal
import json
import requests
from azure.identity import DefaultAzureCredential
from azure.mgmt.rdbms.postgresql import PostgreSQLManagementClient

def postgreySQL_ssl(resourceGroupName, serverName):

    '''{
    "cloud": "azure",
    "policy_type": "Database Management",
    "policy": "azure_SSL_connection_disable_postgreSQL_database_custom_enforcement",
    "custom_env": {
        "resourceGroupName": "cloud-custodian",
        "serverName": "custodiankeyvolt"
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
            "sslEnforcement": 'Enabled'
        }
    }

    payload = json.dumps(payload)

    url = f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resourceGroupName}/providers/Microsoft.DBforPostgreSQL/servers/{serverName}?api-version=2017-12-01'
    response = requests.request("PATCH", url, headers=headers, data=payload)

    return ".done.\n" + response.text


def postgreySQL_log_checkpoints(resourceGroupName, serverName):

    '''{
    "cloud": "azure",
    "policy_type": "Database Management",
    "policy": "azure_postgreSQL_log_checkpoints_custom_enforcement",
    "custom_env": {
        "resourceGroupName": "cloud-custodian",
        "serverName": "custodiankeyvolt"
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
                "value":[{
                "name": "log_checkpoints",
                "properties": {
                    "value": "on"
                         }}
                ]
              }

    payload = json.dumps(payload)

    url = f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resourceGroupName}/providers/Microsoft.DBforPostgreSQL/servers/{serverName}/updateConfigurations?api-version=2017-12-01'
    response2 = requests.request("POST", url, headers=headers, data=payload)

    return ".done.\n" + response2.text


def postgreySQL_connection_throttling(resourceGroupName, serverName):

    '''{
    "cloud": "azure",
    "policy_type": "Database Management",
    "policy": "azure_PostgreSQL_log_connection_throttling_custom_enforcement",
    "custom_env": {
        "resourceGroupName": "cloud-custodian",
        "serverName": "custodiankeyvolt"
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
                "value":[{
                "name": "connection_throttling",
                "properties": {
                    "value": "on"
                         }}
                ]
              }

    payload = json.dumps(payload)

    url = f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resourceGroupName}/providers/Microsoft.DBforPostgreSQL/servers/{serverName}/updateConfigurations?api-version=2017-12-01'
    response2 = requests.request("POST", url, headers=headers, data=payload)

    return ".done.\n" + response2.text


def postgreySQL_log_connections(resourceGroupName, serverName):

    '''{
    "cloud": "azure",
    "policy_type": "Database Management",
    "policy": "azure_PostgreSQL_log_connections_custom_enforcement",
    "custom_env": {
        "resourceGroupName": "cloud-custodian",
        "serverName": "custodiankeyvolt"
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
                "value":[{
                "name": "log_connections",
                "properties": {
                    "value": "on"
                         }}
                ]
              }

    payload = json.dumps(payload)

    url = f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resourceGroupName}/providers/Microsoft.DBforPostgreSQL/servers/{serverName}/updateConfigurations?api-version=2017-12-01'
    response2 = requests.request("POST", url, headers=headers, data=payload)

    return ".done.\n" + response2.text


def postgreySQL_log_disconnections(resourceGroupName, serverName):

    '''{
    "cloud": "azure",
    "policy_type": "Database Management",
    "policy": "azure_postgreSQL_log_checkpoints_custom_enforcement",
    "custom_env": {
        "resourceGroupName": "cloud-custodian",
        "serverName": "custodiankeyvolt"
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
                "value":[{
                "name": "log_disconnections",
                "properties": {
                    "value": "on"
                         }}
                ]
              }

    payload = json.dumps(payload)

    url = f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resourceGroupName}/providers/Microsoft.DBforPostgreSQL/servers/{serverName}/updateConfigurations?api-version=2017-12-01'
    response2 = requests.request("POST", url, headers=headers, data=payload)

    return ".done.\n" + response2.text


def postgreySQL_log_retention_days(resourceGroupName, serverName,retention_day):

    '''{
    "cloud": "azure",
    "policy_type": "Database Management",
    "policy": "azure_PostgreSQL_log_retention_custom_enforcement",
    "custom_env": {
        "resourceGroupName": "cloud-custodian",
        "serverName": "custodiankeyvolt",
        "retention_day": "2"
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
                "value":[{
                "name": "log_retention_days",
                "properties": {
                    "value": f"{retention_day}"
                         }}
                ]
              }

    payload = json.dumps(payload)

    url = f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resourceGroupName}/providers/Microsoft.DBforPostgreSQL/servers/{serverName}/updateConfigurations?api-version=2017-12-01'
    response2 = requests.request("POST", url, headers=headers, data=payload)

    return ".done.\n" + response2.text