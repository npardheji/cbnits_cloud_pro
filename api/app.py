from subprocess import Popen, PIPE, STDOUT
from module.Azure.activityLog import azure_activityLog
from module.Azure.msdefender_enable import azure_msdefender_storage_enable
from module.Azure.soft_delete import  azure_soft_delete
from module.Azure.msdefender_enable import azure_msdefender_app_service_enable
from module.Azure.msdefender_enable import azure_msdefender_SqlServerVirtualMachines_enable
from module.Azure.msdefender_enable import azure_msdefender_ContainerRegistry_enable
from module.Azure.msdefender_enable import azure_msdefender_KeyVaults_enable
from module.Azure.net_watcher import network_watcher
from module.Azure.webapp_actions import webappCreate,webappftp,webappHttpsLetest,webappTls,webappHttpToHttps,webappPythonVersion,webappJavaVersion,webappGoVersion,webappPhpVersion,webappNodeVersion,webappNetVersion,webappWindowsJavaVersion,webappWindowsNetVersion,webappWindowsNodeVersion,webappADenable,webappAuth,webappClient,webappHealth, webappRemoteDebug,webappHttpsLogging
from module.Azure.postgreySQL_actions import postgreySQL_ssl,postgreySQL_log_checkpoints,postgreySQL_connection_throttling,postgreySQL_log_connections,postgreySQL_log_disconnections,postgreySQL_log_retention_days
from module.Azure.nsg_flowlog import flowlog
from module.Azure.nsg_rule import nsg_security_rule,nsg_security_rule_allow
from module.Azure.resource_group import resource_group_lock
from module.Azure.mySQL_actions import mysqlTls
from module.Azure.sql_actions import sqlTDE
from module.Azure.app_gateway_actions import app_WAF


import os
import json
import traceback
import yaml
from pprint import pprint
from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    return "<p>Custodian End points</p>"

@app.route("/get-envs", methods=['GET'])
def get_env_vars():
    env_variables = {key:val for key, val in os.environ.items()}
    return {"status":200, "resp": env_variables}    

@app.route("/set-azure-env", methods=['POST'])
def set_azure_env():  
    os.environ["AZURE_CLIENT_ID"] = request.json['AZURE_CLIENT_ID']
    os.environ["AZURE_CLIENT_SECRET"] = request.json['AZURE_CLIENT_SECRET']
    os.environ["AZURE_TENANT_ID"] = request.json['AZURE_TENANT_ID']
    os.environ["AZURE_SUBSCRIPTION_ID"] = request.json['AZURE_SUBSCRIPTION_ID']

    return {"status":200, "resp": "ENV vars setup successfully"}

@app.route("/set-aws-env", methods=['POST'])
def set_aws_env():  
    os.environ["AWS_ACCESS_KEY_ID"] = request.json['AWS_ACCESS_KEY_ID']
    os.environ["AWS_SECRET_ACCESS_KEY"] = request.json['AWS_SECRET_ACCESS_KEY']
    os.environ["AWS_DEFAULT_REGION"] = request.json['AWS_DEFAULT_REGION']  

    return {"status":200, "resp": "ENV vars setup successfully"}

@app.route('/run-policy', methods=['POST'])
def run_policy():
    try:
        print("Started to run the policy...")
        resource_resp = None
        cloud=request.json['cloud']
        policy_type=request.json['policy_type']
        policy_name=request.json['policy']

        output_policy_path = "{}/out/{}/resources.json".format(os.getcwd(), policy_name)
        if os.path.exists(output_policy_path):
            os.remove(output_policy_path)
            print("Deleted existing resources.json")

        # cmd = "custodian run --help"
        cmd = "custodian run -s out {}/policies/{}/{}/{}.yaml".format(os.getcwd(),cloud, policy_type, policy_name)
        process = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
        cli_resp = process.communicate()[0].decode("utf-8")

        # capturing and return the json output
        if os.path.exists(output_policy_path):
            f = open(output_policy_path)
            resource_resp = json.load(f)

        return {"status":200, "resp": resource_resp, "cli_resp": cli_resp}

    except Exception as err:
        print("Error",err)
        traceback.print_exc()
        return {"status":500, "resp": err}








@app.route('/custom-policy', methods=['POST'])
def custom_policy():
    try:
        print("Started to run the policy...")
        cloud=request.json['cloud']
        policy_type=request.json['policy_type']
        policy_name=request.json['policy']
        custom_env=request.json['custom_env']
       
        cmd = "{}/policies/{}/{}/{}.yaml".format(os.getcwd(),cloud, policy_type, policy_name)
        with open(cmd, "r") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
            
            if any([True for k,v in data['policies'][0].items() if v == "azure.activityLog"]):

                resourceGroupName=request.json['resourceGroupName']
                retentiondays=request.json['retentiondays']
                   
                return {"status":200, "resp": azure_activityLog(resourceGroupName, retentiondays)}

            elif any([True for k,v in data['policies'][0].items() if v == "azure.defender-storage"]):
                return {"status":200, "resp": azure_msdefender_storage_enable()}
            elif any([True for k,v in data['policies'][0].items() if v == "azure.defender-app_service"]):
                return {"status":200, "resp": azure_msdefender_app_service_enable()}
            elif any([True for k,v in data['policies'][0].items() if v == "azure.defender-SqlServerVirtualMachines"]):
                return {"status":200, "resp": azure_msdefender_SqlServerVirtualMachines_enable()}
            elif any([True for k,v in data['policies'][0].items() if v == "azure.defender-ContainerRegistry"]):
                return {"status":200, "resp": azure_msdefender_ContainerRegistry_enable()}
            elif any([True for k,v in data['policies'][0].items() if v == "azure.defender-KeyVaults"]):
                return {"status":200, "resp": azure_msdefender_KeyVaults_enable()}


            
            
            #------------------------------------------  NETWORK  ----------------------------------------------------

            elif any([True for k,v in data['policies'][0].items() if v == "azure.networkwatcher"]):
                return {"status":200, "resp": network_watcher()}
            
            elif any([True for k,v in data['policies'][0].items() if v == "azure.nsg-flow-log"]):
                resourceGroupName=custom_env['resourceGroupName']
                nsg_name=custom_env['nsg_name']
                storage=custom_env['storage']
                retention_day=custom_env['retention_day']
                netwatcher=custom_env['netwatcher']
                return {"status":200, "resp": flowlog(resourceGroupName,nsg_name,storage,retention_day,netwatcher)}

            elif any([True for k,v in data['policies'][0].items() if v == "azure.resource_lock"]):
                resourceGroupName=custom_env['resourceGroupName']
                return {"status":200, "resp": resource_group_lock(resourceGroupName)}


            
            #---------------------------------- PostgreySQL --------------------------------------------

            elif any([True for k, v in data['policies'][0].items() if v == "azure.postgreySQL-ssl"]):
                resourceGroupName = custom_env['resourceGroupName']
                serverName = custom_env['serverName']
                return {"status": 200, "resp": postgreySQL_ssl(resourceGroupName, serverName)}

            elif any([True for k, v in data['policies'][0].items() if v == "azure.postgreysql-log-checkpoint"]):
                resourceGroupName = custom_env['resourceGroupName']
                serverName = custom_env['serverName']
                return {"status": 200, "resp": postgreySQL_log_checkpoints(resourceGroupName, serverName)}
            
            elif any([True for k, v in data['policies'][0].items() if v == "azure.postgreysql-log-connection"]):
                resourceGroupName = custom_env['resourceGroupName']
                serverName = custom_env['serverName']
                return {"status": 200, "resp": postgreySQL_log_connections(resourceGroupName, serverName)}

            elif any([True for k, v in data['policies'][0].items() if v == "azure.postgreysql-log-disconnection"]):
                resourceGroupName = custom_env['resourceGroupName']
                serverName = custom_env['serverName']
                return {"status": 200, "resp": postgreySQL_log_disconnections(resourceGroupName, serverName)}

            elif any([True for k, v in data['policies'][0].items() if v == "azure.postgreysql-connection-throttling"]):
                resourceGroupName = custom_env['resourceGroupName']
                serverName = custom_env['serverName']
                return {"status": 200, "resp": postgreySQL_connection_throttling(resourceGroupName, serverName)}

            elif any([True for k, v in data['policies'][0].items() if v == "azure.postgreysql-log-retention"]):
                resourceGroupName = custom_env['resourceGroupName']
                serverName = custom_env['serverName']
                retention_day=custom_env['retention_day']
                return {"status": 200, "resp": postgreySQL_log_retention_days(resourceGroupName, serverName,retention_day)}
        
            # --------------------------- MySQL -----------------

            elif any([True for k, v in data['policies'][0].items() if v == "azure.mysqlTls"]):
                resourceGroupName = custom_env['resourceGroupName']
                serverName = custom_env['serverName']
                return {"status": 200, "resp": mysqlTls(resourceGroupName, serverName)}

            # --------------------- SQL -----------

            elif any([True for k, v in data['policies'][0].items() if v == "azure.sql-TDE"]):
                resourceGroupName = custom_env['resourceGroupName']
                serverName = custom_env['serverName']
                databaseName = custom_env['databaseName']
                return {"status": 200, "resp": sqlTDE(resourceGroupName, serverName,databaseName)}

            #------------------------- APP GATEWAY ----------------------

            elif any([True for k, v in data['policies'][0].items() if v == "azure.appGateway-waf"]):
                resourceGroupName = custom_env['resourceGroupName']
                applicationGatewayName = custom_env['applicationGatewayName']
                return {"status": 200, "resp": app_WAF(resourceGroupName, applicationGatewayName)}




# --------------------------------------------  NSG RULE ----------------------------------------------------------------

            elif any([True for k,v in data['policies'][0].items() if v == "azure.nsgRule"]):
                resourceGroupName=custom_env['resourceGroupName']
                nsg_name=custom_env['nsg_name']

                direction= data['policies'][0]['direction']
                access= data['policies'][0]['access']
                protocol=data['policies'][0]['protocol']
                destination_port_range= data['policies'][0]['destination_port_range']
                destination_address_prefix= data['policies'][0]['destination_address_prefix']
                source_port_range= data['policies'][0]['source_port_range']
                source_address_prefix= custom_env['source_add']
                return {"status":200, "resp": nsg_security_rule(resourceGroupName, nsg_name, source_address_prefix, direction, access, protocol,destination_port_range, destination_address_prefix, source_port_range)}


            

           

            


           

            # elif any([True for k,v in data['policies'][0].items() if v == "azure.nsgRule_TCP1433"]):
            #     resourceGroupName=custom_env['resourceGroupName']
            #     nsg_name=custom_env['nsg_name']
            #     protocols="TCP"
            #     source_add=custom_env['source_add'] 
            #     dport="1433"
            #     return {"status":200, "resp": nsg_security_rule(resourceGroupName, nsg_name, protocols,source_add,dport)}

            # elif any([True for k,v in data['policies'][0].items() if v == "azure.nsgRule_TCP23"]):
            #     resourceGroupName=custom_env['resourceGroupName']
            #     nsg_name=custom_env['nsg_name']
            #     protocols="TCP"
            #     source_add=custom_env['source_add'] 
            #     dport="23"
            #     return {"status":200, "resp": nsg_security_rule(resourceGroupName, nsg_name, protocols,source_add,dport)}

            # elif any([True for k,v in data['policies'][0].items() if v == "azure.nsgRule_TCP5500"]):
            #     resourceGroupName=custom_env['resourceGroupName']
            #     nsg_name=custom_env['nsg_name']
            #     protocols="TCP"
            #     source_add=custom_env['source_add'] 
            #     dport="5500"
            #     return {"status":200, "resp": nsg_security_rule(resourceGroupName, nsg_name, protocols,source_add,dport)}

            # elif any([True for k,v in data['policies'][0].items() if v == "azure.nsgRule_TCP5900"]):
            #     resourceGroupName=custom_env['resourceGroupName']
            #     nsg_name=custom_env['nsg_name']
            #     protocols="TCP"
            #     source_add=custom_env['source_add'] 
            #     dport="5900"
            #     return {"status":200, "resp": nsg_security_rule(resourceGroupName, nsg_name, protocols,source_add,dport)}

            # elif any([True for k,v in data['policies'][0].items() if v == "azure.nsgRule_TCP135"]):
            #     resourceGroupName=custom_env['resourceGroupName']
            #     nsg_name=custom_env['nsg_name']
            #     protocols="TCP"
            #     source_add=custom_env['source_add'] 
            #     dport="135"
            #     return {"status":200, "resp": nsg_security_rule(resourceGroupName, nsg_name, protocols,source_add,dport)}

            # elif any([True for k,v in data['policies'][0].items() if v == "azure.nsgRule_TCP445"]):
            #     resourceGroupName=custom_env['resourceGroupName']
            #     nsg_name=custom_env['nsg_name']
            #     protocols="TCP"
            #     source_add=custom_env['source_add'] 
            #     dport="445"
            #     return {"status":200, "resp": nsg_security_rule(resourceGroupName, nsg_name, protocols,source_add,dport)}

            # elif any([True for k,v in data['policies'][0].items() if v == "azure.nsg_allow_1270"]):
            #     resourceGroupName=custom_env['resourceGroupName']
            #     nsg_name=custom_env['nsg_name']
            #     protocols="*"
            #     source_add=custom_env['source_add'] 
            #     dport="1270"
            #     return {"status":200, "resp": nsg_security_rule_allow(resourceGroupName, nsg_name, protocols,source_add,dport)}

            # elif any([True for k,v in data['policies'][0].items() if v == "azure.nsg_allow_5985"]):
            #     resourceGroupName=custom_env['resourceGroupName']
            #     nsg_name=custom_env['nsg_name']
            #     protocols="*"
            #     source_add=custom_env['source_add'] 
            #     dport="5985"
            #     return {"status":200, "resp": nsg_security_rule_allow(resourceGroupName, nsg_name, protocols,source_add,dport)}

            # elif any([True for k,v in data['policies'][0].items() if v == "azure.nsg_allow_5986"]):
            #     resourceGroupName=custom_env['resourceGroupName']
            #     nsg_name=custom_env['nsg_name']
            #     protocols="*"
            #     source_add=custom_env['source_add'] 
            #     dport="5986"
            #     return {"status":200, "resp": nsg_security_rule_allow(resourceGroupName, nsg_name, protocols,source_add,dport)}

            # elif any([True for k,v in data['policies'][0].items() if v == "azure.nsgRule_actions"]):
            #     #print("..................................",data['policies'][0]['protocot'])
            #     resourceGroupName=custom_env['resourceGroupName']
            #     nsg_name=custom_env['nsg_name']
            #     protocols="*"
            #     source_add=custom_env['source_add'] 
            #     dport="5986"
            #     return {"status":200, "resp": nsg_security_rule_allow(resourceGroupName, nsg_name, protocols,source_add,dport)}

            


#.......................................  WEB-APP ....................................................

            elif any([True for k,v in data['policies'][0].items() if v == "azure.webappCreate"]):
                resourceGroupName=custom_env['resourceGroupName']
                location=custom_env['location']
                return {"status":200, "resp": webappCreate(resourceGroupName,location)}
                
            elif any([True for k,v in data['policies'][0].items() if v == "azure.webappftp"]):
                resourceGroupName=custom_env['resourceGroupName']
                appName=custom_env['appName']
                location=custom_env['location']
                return {"status":200, "resp": webappftp(resourceGroupName,appName,location)}

            elif any([True for k, v in data['policies'][0].items() if v == "azure.webappHttpsLetest"]):
                resourceGroupName = custom_env['resourceGroupName']
                appname = custom_env['appname']
                return {"status": 200, "resp": webappHttpsLetest(resourceGroupName, appname)}

            elif any([True for k, v in data['policies'][0].items() if v == "azure.webappHttpsOnly-function"]):
                resourceGroupName = custom_env['resourceGroupName']
                appname = custom_env['appname']
                return {"status": 200, "resp": webappHttpToHttps(resourceGroupName, appname)}

            elif any([True for k, v in data['policies'][0].items() if v == "azure.webappHttpsOnly"]):
                resourceGroupName = custom_env['resourceGroupName']
                appname = custom_env['appname']
                return {"status": 200, "resp": webappHttpToHttps(resourceGroupName, appname)}

            elif any([True for k, v in data['policies'][0].items() if v == "azure.webappTls"]):
                resourceGroupName = custom_env['resourceGroupName']
                appname = custom_env['appname']
                return {"status": 200, "resp": webappTls(resourceGroupName, appname)}

            elif any([True for k, v in data['policies'][0].items() if v == "azure.webappTls-function"]):
                resourceGroupName = custom_env['resourceGroupName']
                appname = custom_env['appname']
                return {"status": 200, "resp": webappTls(resourceGroupName, appname)}

            elif any([True for k, v in data['policies'][0].items() if v == "azure.webappPhp"]):
                resourceGroupName = custom_env['resourceGroupName']
                appname = custom_env['appname']
                return {"status": 200, "resp": webappPhpVersion(resourceGroupName, appname)}

            elif any([True for k, v in data['policies'][0].items() if v == "azure.webappJava"]):
                resourceGroupName = custom_env['resourceGroupName']
                appname = custom_env['appname']
                return {"status": 200, "resp": webappJavaVersion(resourceGroupName, appname)}

            elif any([True for k, v in data['policies'][0].items() if v == "azure.webappNode"]):
                resourceGroupName = custom_env['resourceGroupName']
                appname = custom_env['appname']
                return {"status": 200, "resp": webappNodeVersion(resourceGroupName, appname)}

            elif any([True for k, v in data['policies'][0].items() if v == "azure.webappGo"]):
                resourceGroupName = custom_env['resourceGroupName']
                appname = custom_env['appname']
                return {"status": 200, "resp": webappGoVersion(resourceGroupName, appname)}

            elif any([True for k, v in data['policies'][0].items() if v == "azure.webappPython"]):
                resourceGroupName = custom_env['resourceGroupName']
                appname = custom_env['appname']
                return {"status": 200, "resp": webappPythonVersion(resourceGroupName, appname)}

            elif any([True for k, v in data['policies'][0].items() if v == "azure.webappNet"]):
                resourceGroupName = custom_env['resourceGroupName']
                appname = custom_env['appname']
                return {"status": 200, "resp": webappNetVersion(resourceGroupName, appname)}

            elif any([True for k, v in data['policies'][0].items() if v == "azure.webappJava-windows"]):
                resourceGroupName = custom_env['resourceGroupName']
                appname = custom_env['appname']
                return {"status": 200, "resp": webappWindowsJavaVersion(resourceGroupName, appname)}

            elif any([True for k, v in data['policies'][0].items() if v == "azure.webappNode-windows"]):
                resourceGroupName = custom_env['resourceGroupName']
                appname = custom_env['appname']
                return {"status": 200, "resp": webappWindowsNodeVersion(resourceGroupName, appname)}

            elif any([True for k, v in data['policies'][0].items() if v == "azure.webappNet-windows"]):
                resourceGroupName = custom_env['resourceGroupName']
                appname = custom_env['appname']
                return {"status": 200, "resp": webappWindowsNetVersion(resourceGroupName, appname)}

            elif any([True for k, v in data['policies'][0].items() if v == "azure.webapp-AD"]):
                resourceGroupName = custom_env['resourceGroupName']
                appname = custom_env['appname']
                return {"status": 200, "resp": webappADenable(resourceGroupName, appname)}

            elif any([True for k, v in data['policies'][0].items() if v == "azure.webapp-Auth"]):
                resourceGroupName = custom_env['resourceGroupName']
                appname = custom_env['appname']
                return {"status": 200, "resp": webappAuth(resourceGroupName, appname)}

            elif any([True for k, v in data['policies'][0].items() if v == "azure.webapp-client"]):
                resourceGroupName = custom_env['resourceGroupName']
                appname = custom_env['appname']
                return {"status": 200, "resp": webappClient(resourceGroupName, appname)}

            elif any([True for k, v in data['policies'][0].items() if v == "azure.webapp-health"]):
                resourceGroupName = custom_env['resourceGroupName']
                appname = custom_env['appname']
                healthCheckPath=custom_env['healthCheckPath']
                return {"status": 200, "resp": webappHealth(resourceGroupName, appname,healthCheckPath)}
            
            elif any([True for k, v in data['policies'][0].items() if v == "azure.webapp-debug"]):
                resourceGroupName = custom_env['resourceGroupName']
                appname = custom_env['appname']
                return {"status": 200, "resp": webappRemoteDebug(resourceGroupName, appname)}

            elif any([True for k, v in data['policies'][0].items() if v == "azure.webapp-httplog"]):
                resourceGroupName = custom_env['resourceGroupName']
                appname = custom_env['appname']
                return {"status": 200, "resp": webappHttpsLogging(resourceGroupName, appname)}


            else:
                return {"status":"error"}

    except Exception as err:
        print("Error",err)
        traceback.print_exc()
        return {"status":500, "resp": err}


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')       


