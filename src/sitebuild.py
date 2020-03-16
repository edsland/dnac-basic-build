import json
import requests
import time
from dnacentersdk import api
from dnacentersdk.exceptions import ApiError

#open cred file for dnac connection establishment
with open('cred.json') as json_file:
    cred = json.load(json_file)

dnac = api.DNACenterAPI(base_url=cred['dnacurl'],
username=cred['username'],password=cred['passwd'], verify=False)


def create_mysites():
    with open('sites.json') as json_file:
        sites = json.load(json_file)
    
    try: 
        for item in sites['site']:
            #print(sites['site'][item])
            data = {}
            data[item] = sites['site'][item]
            print('++++++++++++++++++++++++++++++++++++++++')
            print('Creating {ptype} named: {pname}'.format(ptype=item, pname=data[item]['name']))
            print('++++++++++++++++++++++++++++++++++++++++')
            dnac.sites.create_site(site=data, type=item)
            time.sleep(1)
    except ApiError as e:
            print(e)
  
def create_myglobalpool():
    with open('pools.json') as json_file:
        pools = json.load(json_file)
    headers={"content-type" : "application/json", "__runsync" : "True"}
    url = 'dna/intent/api/v1/global-pool'
    payload = pools

    try:
        status = dnac.custom_caller.call_api(method="POST", resource_path=url, headers=headers, data=json.dumps(payload))
        print(json.dumps(status, indent=2))
    except ApiError as e:
            print(e)
    


#create_mysites()
#create_myglobalpool()
#create_mycredentials()

