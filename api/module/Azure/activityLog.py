from azure.mgmt.monitor import MonitorManagementClient
from azure.identity import DefaultAzureCredential
from datetime import timedelta 
import datetime
import os


def azure_activityLog(resourceGroupName, retentiondays):

    subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
    
    credentials = DefaultAzureCredential() 
    client = MonitorManagementClient(
        credentials,
        subscription_id
    )

    today = datetime.datetime.now().date()
    retentiondays = retentiondays
    retention = today - timedelta(retentiondays)
    resourceGroupName= resourceGroupName
    # filter = " and ".join([ "eventTimestamp ge '2022-01-01T09:27:40Z' and eventTimestamp le '{}T00:00:00Z'".format(today), "resourceGroupName eq 'cloud-custodian'" ])
    # filter = " and ".join([ "eventTimestamp ge '{}T09:27:40Z'".format(Retention), "and eventTimestamp le '{}T00:00:00Z'".format(today), "resourceGroupName eq 'cloud-custodian'" ])
    filter = " and ".join([ "eventTimestamp ge '{}T00:00:00Z'".format(retention), "eventTimestamp le '{}T00:00:00Z'".format(today), "resourceGroupName eq '{}'".format(resourceGroupName) ])

    select = ",".join([ "eventName", "operationName" ])

    activity_logs = client.activity_logs.list( filter=filter, select=select )
    

    output_dict= []
    for log in activity_logs:
        a= " ".join([log.event_name.localized_value,log.operation_name.localized_value])
        output_dict.append(a)
    return (output_dict)