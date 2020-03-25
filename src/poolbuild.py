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


def task_status(taskid=None):
    #this function is used to get task status, it returns the json response
    headers={"content-type" : "application/json", "__runsync" : "True"}
    url = 'dna/intent/api/v1/task/' + taskid
    try:
        response = dnac.custom_caller.call_api(method="GET", resource_path=url, headers=headers)
        #print(json.dumps(response, indent=2))
        return response
    except ApiError as e:
        print(e)

def get_mysites(name=None):
    #this function is used to retrieve site id when supplied with a site hierarchy name, ex Global/UK-LONDON
    try: 
        if name is None:
            response = dnac.sites.get_site()
            return response
        else:
            nsplit = name.split("/")
            uname = nsplit[-1]
            response = dnac.sites.get_site(name=name)
            for id in response['response']:
                #pprint.pprint(id)
                if uname == id['name']:
                    return id['id']
            print("Please try using a valid site name!")
    except ApiError as e:
            print(e)
  
def create_myglobalpool():
    #this function is used to create a global ip pools based on info in json file
    with open('pools.json') as json_file:
        data = json.load(json_file)
 
    headers={"content-type" : "application/json", "__runsync" : "True"}
    url = 'api/v2/ippool'
    payload = data['globalpool']

    try:
        response = dnac.custom_caller.call_api(method="POST", resource_path=url, headers=headers, data=json.dumps(payload))
        #return response['response']['taskId']
        status = task_status(response['response']['taskId'])

        if status['response']['isError'] != False:
            print(status['response']['failureReason'])
        else:
            #print(status['response']['progress'])
            print ('Creating IP pool {}'.format(payload["ipPoolName"]))
    except ApiError as e:
        print(e)

def create_mysitepool(siteid, puuid):
    #this function is used to create a site ip pools based on info in json file
    with open('pools.json') as json_file:
        data = json.load(json_file)

    #loop through data dictionary and update siteid and parentuuid for each child pool to be created
    for i in data['sitepool']:
        i['siteId'] = siteid
        for  s in i['ipPools']:
            s.update({"parentUuid": puuid})
    #pprint.pprint(data)
    
    url = 'api/v2/ippool/group'
    headers={"content-type" : "application/json", "__runsync" : "True"}
    payload = data['sitepool']
    
    for i in payload:
        try:
            response = dnac.custom_caller.call_api(method="POST", resource_path=url, headers=headers, data=json.dumps(i))
            status = task_status(response['response']['taskId'])

            if status['response']['isError'] != False:
                print(status['response']['failureReason'])
            else:
                print(status['response']['progress'])
                #print ('Creating IP pool {}'.format(i["groupName"]))
        except ApiError as e:   
            print(e)

def get_pool(name=None):
    #this function is used to retrieve uuid of global ip pool also known as puuid, when supplied with a global ip pool name
    headers={"content-type" : "application/json", "__runsync" : "True"}
    url = 'dna/intent/api/v1/global-pool'

    try:
        if name is None:
            response = dnac.custom_caller.call_api(method="GET", resource_path=url, headers=headers)
            print("Please try using a valid Global pool name!")
            return response
        else:
            response = dnac.custom_caller.call_api(method="GET", resource_path=url, headers=headers)
            for i in response['response']:
                if name == i['ipPoolName']:
                    return i['id']     
    except ApiError as e:
            print(e)


#get site id 
siteid = get_mysites('Global/UK-LONDON/PARK HOUSE')

#create global pool based on supplied json file
create_myglobalpool()

#get parent uuid
puuid= get_pool('Global-Pool1')

#create site pools based on supplied json file
create_mysitepool(siteid, puuid)
