# DNA Center Basic Build
This repo contain a few Python scripts to help you quickly stand up DNAC Center basic configurations.
This script is intended for people that need to repetitively stand up DNA Centers or have demo/poc environments that can be spun up and down.

The scripts are grouped as follows:

## Site Build
This script builds site hierarchy, device cedrentials and network settings at the Global site level.

> !Warning the current version of this script assumes there are no previous device credentials and will proceed to create news one.
In the event there's an existing global device credentials present. These will be deleted and replace with supplied credentials.
>

#### JSON files to use:
sites.json - this file describes design elememts such as area, building, floors, etc
dev-cred.json - this file details global device credential settings such as CLI, SNMP, HTTP, etc
netsettings.json - this file includes global network settings such as NTP, SNMP, Syslog, tec

## IP Pool Build
This script builds IP Pools, starting with creating Global pool(s) and reserving site specific pools. Example of the json file required to create IP pools is includes in this repo.

#### JSON file to use:
pools.json - this file details IP Address Pool allocations at global and site level


## Network Discovery
This script instantiate network discovery to start adding devices into DNAC for management. This script leverages the Global site device credentials to kick off discoveries. My example shows issuing three network discoveries.

#### JSON file to use:
disco.json - this file describes discovery settings to initiate device discovery

