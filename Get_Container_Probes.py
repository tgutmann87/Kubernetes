import os
import csv
import sys
import json

i=0

includeStartupProbe = True
includeLivenessProbe = True
includeReadinessProbe = True

# Array Configuration Items [Http GET, Failure Threshold, Initial Delay Seconds, Period Seconds, Success Threshold, Timeout Seconds]
probeConfig = [True, True, True, True, True, True]

with open('Container_Probe_Information.csv', 'w', newline='') as file:
    file = csv.writer(file)
    row = ['Namespace', 'Pod Name', 'Container Name']

#Startup Probe Headers
    if includeStartupProbe == True:
        if probeConfig[0] == True:
            row.append('SP HttpGet')
        if probeConfig[1] == True:
            row.append('SP FailureThreshold')
        if probeConfig[2] == True:
            row.append('SP InitialDelaySeconds')
        if probeConfig[3] == True:
            row.append('SP PeriodSeconds')
        if probeConfig[4] == True:
            row.append('SP SuccessThreshold')
        if probeConfig[5] == True:
            row.append('SP TimeoutSeconds')
#Liveness Probe Headers
    if includeLivenessProbe == True:
        if probeConfig[0] == True:
            row.append('LP HttpGet')
        if probeConfig[1] == True:
            row.append('LP FailureThreshold')
        if probeConfig[2] == True:
            row.append('LP InitialDelaySeconds')
        if probeConfig[3] == True:
            row.append('LP PeriodSeconds')
        if probeConfig[4] == True:
            row.append('LP SuccessThreshold')
        if probeConfig[5] == True:
            row.append('LP TimeoutSeconds')
#Readiness Probe Headers
    if includeReadinessProbe == True:
        if probeConfig[0] == True:
            row.append('RP HttpGet')
        if probeConfig[1] == True:
            row.append('RP FailureThreshold')
        if probeConfig[2] == True:
            row.append('RP InitialDelaySeconds')
        if probeConfig[3] == True:
            row.append('RP PeriodSeconds')
        if probeConfig[4] == True:
            row.append('RP SuccessThreshold')
        if probeConfig[5] == True:
            row.append('RP TimeoutSeconds')
#Write headers to CSV
    file.writerow(row)
#Running KubeCtl command to get all pods in JSON formatting
    kubectl_output = os.popen('kubectl get pods -A -o json').read()
    kubectl_output = json.loads(kubectl_output)

    for pod in kubectl_output['items']:
        try:
#            if pod['status']['phase'] == 'Running' and pod['metadata']['labels']['product-line'] == 'candp':
            if pod['status']['phase'] == 'Running':
                for container in pod['spec']['containers']:
                    row = [pod['metadata']['namespace'], pod['metadata']['name'], container['name']]
                    if container.get("startupProbe") == None and container.get("livenessProbe") == None and container.get("readinessProbe") == None:
                        row = ""
                    else:
                        if includeStartupProbe == True:
                            if container.get("startupProbe") != None:
                                if container["startupProbe"].get("httpGet") != None:
                                    if probeConfig[0] == True:
                                        row.append(container["startupProbe"].get("httpGet").get("path"))
                                    if probeConfig[1] == True:
                                        row.append(container["startupProbe"].get("failureThreshold", " "))
                                    if probeConfig[2] == True:
                                        row.append(container["startupProbe"].get("initialDelaySeconds", " "))
                                    if probeConfig[3] == True:
                                        row.append(container["startupProbe"].get("periodSeconds", " "))
                                    if probeConfig[4] == True:
                                        row.append(container["startupProbe"].get("successThreshold", " "))
                                    if probeConfig[5] == True:
                                        row.append(container["startupProbe"].get("timeoutSeconds", " "))
                                elif container["startupProbe"].get("exec") != None:
                                    if probeConfig[0] == True:
                                        row.append(container["startupProbe"].get("exec").get("command"))
                                    if probeConfig[1] == True:
                                        row.append(container["startupProbe"].get("failureThreshold", " "))
                                    if probeConfig[2] == True:
                                        row.append(container["startupProbe"].get("initialDelaySeconds", " "))
                                    if probeConfig[3] == True:
                                        row.append(container["startupProbe"].get("periodSeconds", " "))
                                    if probeConfig[4] == True:
                                        row.append(container["startupProbe"].get("successThreshold", " "))
                                    if probeConfig[5] == True:
                                        row.append(container["startupProbe"].get("timeoutSeconds", " "))
                            else:
                                for x in probeConfig:
                                    if x == True:
                                        row.append(' ')
                        if includeLivenessProbe == True:
                            if container.get("livenessProbe") != None:
                                if container["livenessProbe"].get("httpGet") != None:
                                    if probeConfig[0] == True:
                                        row.append(container["livenessProbe"].get("httpGet").get("path"))
                                    if probeConfig[1] == True:
                                        row.append(container["livenessProbe"].get("failureThreshold", " "))
                                    if probeConfig[2] == True:
                                        row.append(container["livenessProbe"].get("initialDelaySeconds", " "))
                                    if probeConfig[3] == True:
                                        row.append(container["livenessProbe"].get("periodSeconds", " "))
                                    if probeConfig[4] == True:
                                        row.append(container["livenessProbe"].get("successThreshold", " "))
                                    if probeConfig[5] == True:
                                        row.append(container["livenessProbe"].get("timeoutSeconds", " "))
                                elif container["livenessProbe"].get("exec") != None:
                                    if probeConfig[0] == True:
                                        row.append(container["livenessProbe"].get("exec").get("command"))
                                    if probeConfig[1] == True:
                                        row.append(container["livenessProbe"].get("failureThreshold", " "))
                                    if probeConfig[2] == True:
                                        row.append(container["livenessProbe"].get("initialDelaySeconds", " "))
                                    if probeConfig[3] == True:
                                        row.append(container["livenessProbe"].get("periodSeconds", " "))
                                    if probeConfig[4] == True:
                                        row.append(container["livenessProbe"].get("successThreshold", " "))
                                    if probeConfig[5] == True:
                                        row.append(container["livenessProbe"].get("timeoutSeconds", " "))
                            else:
                                for x in probeConfig:
                                    if x == True:
                                        row.append(' ')
                        if includeReadinessProbe == True:
                            if container.get("readinessProbe") != None:
                                if container["readinessProbe"].get("httpGet") != None:
                                    if probeConfig[0] == True:
                                        row.append(container["readinessProbe"].get("httpGet").get("path"))
                                    if probeConfig[1] == True:
                                        row.append(container["readinessProbe"].get("failureThreshold", " "))
                                    if probeConfig[2] == True:
                                        row.append(container["readinessProbe"].get("initialDelaySeconds", " "))
                                    if probeConfig[3] == True:
                                        row.append(container["readinessProbe"].get("periodSeconds", " "))
                                    if probeConfig[4] == True:
                                        row.append(container["readinessProbe"].get("successThreshold", " "))
                                    if probeConfig[5] == True:
                                        row.append(container["readinessProbe"].get("timeoutSeconds", " "))
                                elif container["readinessProbe"].get("exec") != None:
                                    if probeConfig[0] == True:
                                        row.append(container["readinessProbe"].get("exec").get("command"))
                                    if probeConfig[1] == True:
                                        row.append(container["readinessProbe"].get("failureThreshold", " "))
                                    if probeConfig[2] == True:
                                        row.append(container["readinessProbe"].get("initialDelaySeconds", " "))
                                    if probeConfig[3] == True:
                                        row.append(container["readinessProbe"].get("periodSeconds", " "))
                                    if probeConfig[4] == True:
                                        row.append(container["readinessProbe"].get("successThreshold", " "))
                                    if probeConfig[5] == True:
                                        row.append(container["readinessProbe"].get("timeoutSeconds", " "))
                            else:
                                for x in probeConfig:
                                    if x == True:
                                        row.append(' ')
                        file.writerow(row)
        except KeyError:
#            print('No Product Line')
            i+= 1
    print(i)
