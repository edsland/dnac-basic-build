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



def get_mysites(name=None):
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
    with open('pools.json') as json_file:
        data = json.load(json_file)

    headers={"content-type" : "application/json", "__runsync" : "True"}
    url = 'api/v2/ippool'
    payload = data
    #for key in data:
    #    payload = data[key]
    #    #pprint.pprint(payload)

    try:
        response = dnac.custom_caller.call_api(method="POST", resource_path=url, headers=headers, data=json.dumps(payload))
        print (response)
    except ApiError as e:
        print(e)
    
def get_pool(name=None):
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
                    print (i['id'])
                    return i['id']

            #pprint.pprint(response)


            
    except ApiError as e:
            print(e)

#site or global, globalpool name

#https://10.53.201.111/api/v2/ippool/group


#create_myglobalpool()
get_pool('Global-Pool2')
#print(get_mysites('Global'))
#get_mysites("Global/UK-LONDON")
