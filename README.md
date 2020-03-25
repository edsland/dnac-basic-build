# DNA Center Basic Build
This repo contain a few Python scripts to help you quickly stand up DNAC Center basic configurations.
This script is intended for people that need to repetitvely stand up DNA Centers or Use for demo/poc environments.

The scripts are grouped as follows:

## Site Build
This script builds site hierarchy, device cedrentials and network settings at the Global site level.

> !Warning the current version of this script assumes there are no previous device credentials and will proceed to create news one.
>
In the event there's an existing global device credentials present. This will delete these and replace with supplied credentials.

## IP Pool Build
This script builds IP Pools, starting with creating Global pool(s) and reserving site specific pools. Example of the json file required to create IP pools is includes in this repo.

## Network Discovery
This script instantiate network discovery to start adding devices into DNAC for management. This script leverages the Global site device credentials to kick off discoveries. My example shows issuing three network discoveries.


