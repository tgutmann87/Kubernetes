import os
import csv
import sys
import json
import requests
from multiprocessing import Pool
from itertools import product

def sendRequest(url):
    endpoint = 'https://' + url[0] + url[1]
        
    try:
        response = requests.get(endpoint, timeout=3)
        if response.status_code >= 200 and response.status_code <= 399:
#            print(endpoint, response.status_code, len(response.content))
           return[endpoint, response.status_code, len(response.content)]
    except requests.exceptions.ConnectTimeout:
#            file.writerow([endpoint, 'Timeout', 'Timeout'])
        print(endpoint, 'Timeout', 'Timeout')
    except requests.exceptions.ConnectionError:
#            file.writerow([endpoint, 'ConnectionError', 'ConnectionError'])
        print(endpoint, 'ConnectionError', 'ConnectionError')
    finally:
        print(endpoint, response.status_code, len(response.content))

if __name__ == '__main__':
    with open('Container_Probe_Responses.csv', 'w', newline='') as file:
        file = csv.writer(file)
        file.writerow(['URL', 'Status Code', 'Response Size'])

        api = ['/actuator/info', '/actuator/health', '/api/v1/rest/actuator/info', '/api/v1/rest/actuator/health', '/health', '/health/ready']
        ingressUrls = []

        kubectl_output = os.popen('kubectl get pods -A -o json').read()
        kubectl_output = json.loads(kubectl_output)

        for pod in kubectl_output['items']:
            for container in pod['spec']['containers']:
                try:
                    if (not api.count(container['livenessProbe']['httpGet']['path'])) and pod['metadata']['labels']['product-line'] == 'candp':
                        api.append(container['livenessProbe']['httpGet']['path'])
                        
                    if (not api.count(container['readinessProbe']['httpGet']['path'])) and pod['metadata']['labels']['product-line'] == 'candp':
                        api.append(container['readinessProbe']['httpGet']['path'])
                except:
                    print('No Probe Present: ')
        
        for i in api:
            if not i.startswith('/'):
                api[api.index(i)] = '/' + i
        api.sort()
        
        for i in api:
            if api.count(i) > 1:
                api.remove(i)
        
#        print(api)
                    
        kubectl_output = os.popen('kubectl get ingress -A -o json').read()
        kubectl_output = json.loads(kubectl_output)

        for ingress in kubectl_output['items']:
            for rule in ingress['spec']['rules']:
                try:
                    if not ingressUrls.count(rule['host']) and rule['host'].count('va.gov') and ingress['metadata']['labels']['product-line'] == 'candp':
                        ingressUrls.append(rule['host'])
                except:
                    print('No Ingress Host Present')

#        print(ingressUrls)
        
#        ingressUrls = ['google.com', 'yahoo.com', 'bing.com']
#        api = ['/actuator/info', '/actuator/health']
#        print('API Size: ' + str(len(api)) + '\n' + 'Ingress Size: ' + str(len(ingressUrls)))

        pool = Pool()
        response = pool.map_async(sendRequest, product(ingressUrls, api), chunksize=509)
#        print(response.get())
        for r in response.get():
                if not r == None:
                    file.writerow(r)
                    