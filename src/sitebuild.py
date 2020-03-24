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

def get_mysites(name=None):
    #this function is use to retrieve site id when supplied with a site hierarchy name, ex Global/UK-LONDON
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

def create_mysites():
    #this function create site design based on parameters specified in json file
    with open('sites.json') as json_file:
        data = json.load(json_file)
    
    try: 
        for item in data['site']:
            #print(data['site'][item])
            sites = {}
            sites[item] = data['site'][item]
            dnac.sites.create_site(site=sites, type=item)
            time.sleep(2)
        print('Creating site hierarchy!')
    except ApiError as e:
            print(e)
    
def get_mycredentials():
    #this function is use to retrieve global site device credential ids
    headers={"content-type" : "application/json", "__runsync" : "True"}
    url = 'dna/intent/api/v1/device-credential'
    myids= []
    try:
        response = dnac.custom_caller.call_api(method="GET", resource_path=url, headers=headers)
        #print(json.dumps(response, indent=2))

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
   
def build_mycredentials():
    #this function checks if there's an existing device credential if so delete and create new one through the given json file
    if get_mycredentials() != []:
        print('Deleting existing device credentials ...')
        delete_mycredentials()
        print('Updating device credentials ...')
        create_mycredentials()
    else:
        create_mycredentials()
        print('Creating new device credentials ...')
    
def create_mycredentials():
    with open('dev-cred.json') as json_file:
        data = json.load(json_file)
    
    headers={"content-type" : "application/json", "__runsync" : "True"}
    url = 'dna/intent/api/v1/device-credential'
    payload = data

    try:
        response = dnac.custom_caller.call_api(method="POST", resource_path=url, headers=headers, data=json.dumps(payload))
        return response['message']
    except ApiError as e:
        print(e)
        
def delete_mycredentials():
    #this function will delete device credential
    headers={"content-type" : "application/json", "__runsync" : "True"}

    try:
        for id in get_mycredentials():
            url = 'dna/intent/api/v1/device-credential/' + id
            dnac.custom_caller.call_api(method="DELETE", resource_path=url, headers=headers)
    except ApiError as e:
        print(e)

def create_netsettings():
     #### correct script
    #this function create network settings at global level based on parameters specified in json file
    with open('netsettings.json') as json_file:
        data = json.load(json_file)

    headers={"content-type" : "application/json", "__runsync" : "True"}
    url = 'dna/intent/api/v1/network/' + get_mysites('Global')
    payload = data
    
    try:
        response = dnac.custom_caller.call_api(method="POST", resource_path=url, headers=headers, data=json.dumps(payload))
        print(response['message'])
    except ApiError as e:
        print(e)


#testing functions
#get_mycredentials()
#delete_mycredentials()
#create_mycredentials()
#get_mysites('Global')

create_mysites()
build_mycredentials()
create_netsettings()