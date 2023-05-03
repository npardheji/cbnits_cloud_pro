import json
import os
import adal
import requests

def mysqlTls(resourceGroupName, serverName):

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

    url = f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resourceGroupName}/providers/Microsoft.DBforMySQL/flexibleServers/{serverName}?api-version=2021-05-01'
    response = requests.request("PATCH", url, headers=headers, data=payload)

    return ".done.\n" + response.text