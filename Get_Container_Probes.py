import os
import csv
import sys
import json

with open('Container_Probe_Information.csv', 'w', newline='') as file:
    file = csv.writer(file)
    file.writerow(['Namespace', 'Pod Name', 'Container Name', 'LP FailureThreshold', 'LP HttpGet', 'LP InitialDelaySeconds', 'LP PeriodSeconds', 'LP SuccessThreshold', 'LP TimeoutSeconds', 'RP FailureThreshold', 'RP HttpGet', 'RP InitialDelaySeconds', 'RP PeriodSeconds', 'RP SuccessThreshold', 'RP TimeoutSeconds' ])

    kubectl_output = os.popen('kubectl get pods -A -o json').read()
    kubectl_output = json.loads(kubectl_output)

    for pod in kubectl_output['items']:
        try:
            if pod['status']['phase'] == 'Running' and pod['metadata']['labels']['product-line'] == 'candp':
                for container in pod['spec']['containers']:
                    row = [pod['metadata']['namespace'], pod['metadata']['name'], container['name']]

                    try:
                        row.extend(container["livenessProbe"].values())
                        
                        try:
                            row.extend(container["readinessProbe"].values())
                            
                        except:
                            for x in range(0,6):
                                row.append(' ')
                                
                        file.writerow(row)
                        
                    except:
                        for x in range(0,6):
                            row.append(' ')
                        
                        try:
                            row.extend(container["readinessProbe"].values())
                            file.writerow(row)
                           
                        except:
                            row = ''
        except:
            print('No Product Line')
            
    
