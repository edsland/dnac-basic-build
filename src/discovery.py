import json
import requests
import time
import pprint
from dnacentersdk import api
from dnacentersdk.exceptions import ApiError

requests.packages.urllib3.disable_warnings() 

#open cred file for dnac connection establishment
with open('cred.json') as json_file:
    data = json.load(json_file)

dnac = api.DNACenterAPI(base_url=data['dnacurl'],
username=data['username'],password=data['passwd'], verify=False)

def disco_status(taskid = None):
    headers={"content-type" : "application/json", "__runsync" : "True"}
    url = 'dna/intent/api/v1/task/' + taskid
    try:
        response = dnac.custom_caller.call_api(method="GET", resource_path=url, headers=headers)
        #print(json.dumps(response, indent=2))
        return response
    except ApiError as e:
        print(e)

def start_disco():
    with open('disco.json') as json_file:
        data = json.load(json_file)
    
    headers={"content-type" : "application/json", "__runsync" : "True"}
    url = 'dna/intent/api/v1/discovery'
    for i in data:
        payload = (data[i])
        
        try:
            response = dnac.custom_caller.call_api(method="POST", resource_path=url, headers=headers, data=json.dumps(payload))
            #return response['response']['taskId']
            time.sleep(2)
            status = disco_status(response['response']['taskId'])

            if status['response']['isError'] != False:
                print(status['response']['failureReason'])
            else:
                print('Creating discovery {}'.format(payload['name']))
        except ApiError as e:
            print(e)


start_disco()





