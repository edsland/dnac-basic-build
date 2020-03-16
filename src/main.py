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

""" sites = dnac.sites.get_site()
print (sites)
"""

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

dnac.custom_caller.add_api('add_global_ip_pool', 
                            lambda pool:
                            dnac.custom_caller.add_api(
                                'POST',
                                '/dna/intent/api/v1/global-pool',
                                json=pool)
                            )

    
def create_myglobalpool():
    with open('pools.json') as json_file:
        pools = json.load(json_file)
        print(pools['settings'])
        dnac.custom_caller.add_global_ip_pool(pools)
        
    



#create_mysites()
create_myglobalpool()
#create_mycredentials()
