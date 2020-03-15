import yaml
import json
import requests
from dnacentersdk import api

#open cred file for dnac connection establishment
with open('cred.json') as json_file:
    cred = json.load(json_file)

dnac = api.DNACenterAPI(base_url=cred['dnacurl'],
username=cred['username'],password=cred['passwd'], verify=False)

sites = dnac.sites.get_site()
print (sites)

def create_sites():
    dnac.sites.create_site(site=site['sites']['area']['name'], type=area, )
