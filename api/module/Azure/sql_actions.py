import os
import adal
import json
import requests
from azure.identity import DefaultAzureCredential
from azure.mgmt.rdbms.postgresql import PostgreSQLManagementClient

def sqlTDE(resourceGroupName, serverName, databaseName):

    '''{
    "cloud": "azure",
    "policy_type": "Database Management",
    "policy": "azure_data_encryption_on_SQL_custom_enforcement",
    "custom_env": {
        "resourceGroupName": "cloud-custodian",
        "serverName": "mycustomsqlserver",
        "databaseName": "mtycustondb"
    }
        }}'''

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
            "state": "Enabled"
        }
        }

    payload = json.dumps(payload)

    url = f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resourceGroupName}/providers/Microsoft.Sql/servers/{serverName}/databases/{databaseName}/transparentDataEncryption/current?api-version=2022-05-01-preview'
    response = requests.request("PUT", url, headers=headers, data=payload)

    return ".done.\n" + response.text