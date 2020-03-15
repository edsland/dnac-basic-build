import yaml
import requests

#open cred file for 
with open('cred.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

print(data['dnac-server'])
