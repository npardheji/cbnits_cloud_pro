import os
import random
import adal
import requests
import json
from azure.mgmt.web import WebSiteManagementClient
from azure.identity import DefaultAzureCredential


def webappCreate(RESOURCE_GROUP_NAME,LOCATION,):

  """{
    "cloud": "azure",
    "policy_type": "Network",
    "policy": "webappCreate",
    "custom_env": {
        "resourceGroupName": "cloud-custodian",
        "location": "eastus"
        }

    }"""


  subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
  credentials = DefaultAzureCredential()

  # RESOURCE_GROUP_NAME = 'cloud-custodian'
  # LOCATION = "eastus"

  SERVICE_PLAN_NAME = f'service-plan-{random.randint(1,100000):05}'
  WEB_APP_NAME = f"custom-app-{random.randint(1,100000):05}"

  app_service_client = WebSiteManagementClient(credentials, subscription_id)

  poller = app_service_client.app_service_plans.begin_create_or_update(RESOURCE_GROUP_NAME,
      SERVICE_PLAN_NAME,
      {
          "location": LOCATION,
          "reserved": True,
          "sku" : {"name" : "B1"}
      }
  )

  plan_result = poller.result()

  print(f"Provisioned App Service plan {plan_result.name}")



  poller = app_service_client.web_apps.begin_create_or_update(RESOURCE_GROUP_NAME,
      WEB_APP_NAME,
      {
          "location": LOCATION,
          "server_farm_id": plan_result.id,
          "site_config": {
              "linux_fx_version": "python|3.8"
          }
      }
  )

  web_app_result = poller.result()
  print(f"Provisioned web app {web_app_result.name} at {web_app_result.default_host_name}")

  return "WEB APP CREATED"





def webappftp(resourceGroupName,appName,location):
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
        "allow": False
      },
      "location": f"{location}"
    }


    payload=json.dumps(payload)
    
    url=f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/sites/{appName}/basicPublishingCredentialsPolicies/ftp?api-version=2022-03-01'

    response = requests.request("PUT", url, headers=headers, data = payload)
    
    return "...................done..............."+response.text




def webappTls(resourceGroupName, appname):

    '''
    {
    "cloud": "azure",
    "policy_type": "Web App",
    "policy": "azure_webapp_latest_tls_custom_enforcement",
    "custom_env": {
        "resourceGroupName": "cloud-custodian",
        "appname": "chikentanduri"
    }
    }
    '''

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
            "minTlsVersion": "1.2"
        }
    }

    payload = json.dumps(payload)

    url = f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/sites/{appname}/config/web?api-version=2022-03-01'
    response = requests.request("PATCH", url, headers=headers, data=payload)

    return ".done." + response.text
    





def webappPythonVersion(resourceGroupName, appname):

    '''{
    "cloud": "azure",
    "policy_type": "Web App",
    "policy": "azure_webapp_latest_python_version_custom_enforcement",
    "custom_env": {
        "resourceGroupName": "cloud-custodian",
        "appname": "chikentanduri"
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
            "linuxFxVersion": 'PYTHON|3.11'
        }
    }

    payload = json.dumps(payload)

    url = f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/sites/{appname}/config/web?api-version=2022-03-01'
    response = requests.request("PATCH", url, headers=headers, data=payload)

    return ".done.\n" + response.text

def webappJavaVersion(resourceGroupName, appname):

    '''{
    "cloud": "azure",
    "policy_type": "Web App",
    "policy": "webapp_python_3_11",
    "custom_env": {
        "resourceGroupName": "cloud-custodian",
        "appname": "chikentanduri"
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
            "linuxFxVersion": 'JAVA|12-java12'
        }
    }

    payload = json.dumps(payload)

    url = f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/sites/{appname}/config/web?api-version=2022-03-01'
    response = requests.request("PATCH", url, headers=headers, data=payload)

    return ".done.\n" + response.text


def webappPhpVersion(resourceGroupName, appname):

    '''{
    "cloud": "azure",
    "policy_type": "Web App",
    "policy": "webapp_python_3_11",
    "custom_env": {
        "resourceGroupName": "cloud-custodian",
        "appname": "chikentanduri"
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
            "linuxFxVersion": 'PHP|8.1'
        }
    }

    payload = json.dumps(payload)

    url = f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/sites/{appname}/config/web?api-version=2022-03-01'
    response = requests.request("PATCH", url, headers=headers, data=payload)

    return ".done.\n" + response.text


def webappNodeVersion(resourceGroupName, appname):

    '''{
    "cloud": "azure",
    "policy_type": "Web App",
    "policy": "webapp_python_3_11",
    "custom_env": {
        "resourceGroupName": "cloud-custodian",
        "appname": "chikentanduri"
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
            "linuxFxVersion": 'NODE|18-lts'
        }
    }

    payload = json.dumps(payload)

    url = f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/sites/{appname}/config/web?api-version=2022-03-01'
    response = requests.request("PATCH", url, headers=headers, data=payload)

    return ".done.\n" + response.text


def webappGoVersion(resourceGroupName, appname):

    '''{
    "cloud": "azure",
    "policy_type": "Web App",
    "policy": "webapp_python_3_11",
    "custom_env": {
        "resourceGroupName": "cloud-custodian",
        "appname": "chikentanduri"
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
            "linuxFxVersion": 'GO|1.19'
        }
    }

    payload = json.dumps(payload)

    url = f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/sites/{appname}/config/web?api-version=2022-03-01'
    response = requests.request("PATCH", url, headers=headers, data=payload)

    return ".done.\n" + response.text

def webappNetVersion(resourceGroupName, appname):

    '''{
    "cloud": "azure",
    "policy_type": "Web App",
    "policy": "webapp_python_3_11",
    "custom_env": {
        "resourceGroupName": "cloud-custodian",
        "appname": "chikentanduri"
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
            "linuxFxVersion": 'DOTNETCORE|7.0'
        }
    }

    payload = json.dumps(payload)

    url = f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/sites/{appname}/config/web?api-version=2022-03-01'
    response = requests.request("PATCH", url, headers=headers, data=payload)

    return ".done.\n" + response.text


# windows


def webappWindowsJavaVersion(resourceGroupName, appname):

    '''{
    "cloud": "azure",
    "policy_type": "Web App",
    "policy": "webapp_python_3_11",
    "custom_env": {
        "resourceGroupName": "cloud-custodian",
        "appname": "chikentanduri"
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
            "javaVersion": '17'
        }
    }

    payload = json.dumps(payload)

    url = f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/sites/{appname}/config/web?api-version=2022-03-01'
    response = requests.request("PATCH", url, headers=headers, data=payload)

    return ".done.\n" + response.text


def webappWindowsNodeVersion(resourceGroupName, appname):

    '''{
    "cloud": "azure",
    "policy_type": "Web App",
    "policy": "webapp_python_3_11",
    "custom_env": {
        "resourceGroupName": "cloud-custodian",
        "appname": "chikentanduri"
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
            "nodeVersion": '~18'
        }
    }

    payload = json.dumps(payload)

    url = f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/sites/{appname}/config/web?api-version=2022-03-01'
    response = requests.request("PATCH", url, headers=headers, data=payload)

    return ".done.\n" + response.text



def webappADenable(resourceGroupName, appname):

    '''{
    "cloud": "azure",
    "policy_type": "Web App",
    "policy": "webapp_python_3_11",
    "custom_env": {
        "resourceGroupName": "cloud-custodian",
        "appname": "chikentanduri"
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
        "identity": {
            "type": 'SystemAssigned'
        }
    }

    payload = json.dumps(payload)

    url = f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/sites/{appname}?api-version=2022-03-01'
    response = requests.request("PATCH", url, headers=headers, data=payload)

    return ".done.\n" + response.text


def webappAuth(resourceGroupName, appname):

    '''{
    "cloud": "azure",
    "policy_type": "Web App",
    "policy": "webapp_python_3_11",
    "custom_env": {
        "resourceGroupName": "cloud-custodian",
        "appname": "chikentanduri"
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
            "platform": {
                "enabled": True
            }
        }
    }

    payload = json.dumps(payload)

    url = f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/sites/{appname}/config/authsettingsV2?api-version=2022-03-01'
    response = requests.request("PUT", url, headers=headers, data=payload)

    return ".done.\n" + response.text

def webappClient(resourceGroupName, appname):

    '''{
    "cloud": "azure",
    "policy_type": "Monitoring",
    "policy": "custom_azure_health_check_enable_enforcement",
    "custom_env": {
        "resourceGroupName": "cloud-custodian",
        "appname": "chikentanduri",
        "healthCheckPath": "/path"
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
            "clientCertEnabled": True
        }
    }

    payload = json.dumps(payload)

    url = f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/sites/{appname}?api-version=2022-03-01'
   # https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/sites/{appname}?api-version=2022-03-01
    response = requests.request("PATCH", url, headers=headers, data=payload)

    return ".done.\n" + response.text


def webappHealth(resourceGroupName, appname,healthCheckPath):
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
        "properties": {"siteConfig": {
            "autoHealEnabled": True,
            "healthCheckPath": f"{healthCheckPath}"
        }}
    }

    payload = json.dumps(payload)

    url = f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/sites/{appname}?api-version=2022-03-01'
    response = requests.request("PATCH", url, headers=headers, data=payload)

    return ".done.\n" + response.text


def webappRemoteDebug(resourceGroupName, appname):

    '''{
    "cloud": "azure",
    "policy_type": "Web App",
    "policy": "webapp_python_3_11",
    "custom_env": {
        "resourceGroupName": "cloud-custodian",
        "appname": "chikentanduri"
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
            "remoteDebuggingEnabled": True
        }
    }

    payload = json.dumps(payload)

    url = f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/sites/{appname}/config/web?api-version=2022-03-01'
    response = requests.request("PATCH", url, headers=headers, data=payload)

    return ".done.\n" + response.text



def webappWindowsNetVersion(resourceGroupName, appname):

    '''{
    "cloud": "azure",
    "policy_type": "Web App",
    "policy": "webapp_python_3_11",
    "custom_env": {
        "resourceGroupName": "cloud-custodian",
        "appname": "chikentanduri"
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
            "netFrameworkVersion": 'v7.0'
        }
    }

    payload = json.dumps(payload)

    url = f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/sites/{appname}/config/web?api-version=2022-03-01'
    response = requests.request("PATCH", url, headers=headers, data=payload)

    return ".done.\n" + response.text

def webappHttpsLogging(resourceGroupName, appname):
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
            "httpLoggingEnabled": True
        }
    }

    payload = json.dumps(payload)

    url = f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/sites/{appname}/config/web?api-version=2022-03-01'
    response = requests.request("PATCH", url, headers=headers, data=payload)

    return ".done.\n" + response.text


def webappHttpToHttps(resourceGroupName, appname):

    '''{
    "cloud": "azure",
    "policy_type": "Web App",
    "policy": "webapp_http_to_https",
    "custom_env": {
        "resourceGroupName": "cloud-custodian",
        "appname": "chikentanduri"
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
            "httpsOnly": True
        }
    }

    payload = json.dumps(payload)

    url = f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/sites/{appname}?api-version=2022-03-01'
   # https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/sites/{appname}?api-version=2022-03-01
    response = requests.request("PATCH", url, headers=headers, data=payload)

    return ".done.\n" + response.text


def webappHttpsLetest(resourceGroupName, appname):
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
            "http20Enabled": True
        }
    }

    payload = json.dumps(payload)

    url = f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/sites/{appname}/config/web?api-version=2022-03-01'
    response = requests.request("PATCH", url, headers=headers, data=payload)

    return ".done.\n" + response.text