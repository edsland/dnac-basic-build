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

def task_status(taskid = None):
    #this function is used to get task status, it returns the json response
    headers={"content-type" : "application/json", "__runsync" : "True"}
    url = 'dna/intent/api/v1/task/' + taskid
    try:
        response = dnac.custom_caller.call_api(method="GET", resource_path=url, headers=headers)
        #print(json.dumps(response, indent=2))
        return response
    except ApiError as e:
        print(e)

def get_mycredentials():
    #this function is used to retrieve global site device credential ids
    headers={"content-type" : "application/json", "__runsync" : "True"}
    url = 'dna/intent/api/v1/device-credential'
    myids= []
    try:
        response = dnac.custom_caller.call_api(method="GET", resource_path=url, headers=headers)
        #pprint.pprint(response)

        if "message" in response:
            #means device credentials are empty/ none configured
            return []
        else:
            for i in response:
                nest = response[i]
                for id in nest:
                    myids.append((id['id']))
            return myids
    except ApiError as e:
        print(e)

def start_disco(credlist):
    #this function is used to start network discovery jobs based on supplied json file
    if get_mycredentials() != []:
        with open('disco.json') as json_file:
            data = json.load(json_file)
    
        headers={"content-type" : "application/json", "__runsync" : "True"}
        url = 'dna/intent/api/v1/discovery'

        for key in data:
            data[key]['globalCredentialIdList'] = credlist
            payload = data[key]    
            try:
                response = dnac.custom_caller.call_api(method="POST", resource_path=url, headers=headers, data=json.dumps(payload))
                #return response['response']['taskId']
                time.sleep(2)
                status = task_status(response['response']['taskId'])

                if status['response']['isError'] != False:
                    print(status['response']['failureReason'])
                else:
                    print('Creating discovery {}'.format(payload['name']))
            except ApiError as e:
                print(e)  
    else:
        print('Please create new device credentials first before running this script!')
    


#retrieve credential list ids as input for start_disco function to auto-complete json file
credlist = get_mycredentials()

#kickoff discovery process
start_disco(credlist)





