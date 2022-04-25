python-isilon-syncisires-scripts
=================
Sync Isilon  resource (SMB / NFS).


This script is help to create the same resouces (SMB / NFS) from one Isilon clusters to antoher Isilon cluster using API.

The API end point is based on zone.


Prerequisite:
- Must have Zone Administrator Role on the repspective zone.
- Unable to use cluster root account unless is System Zone
- If zone path is different, please run updatezonepath option before run create option.


This script are unofficial and not supported by DellEMC.
Use at your own risk.

####Tested with:

- OneFS v8.2.2.0
- Python 2.7.6


Change History:
1.0  - init release
1.1  - Bug fix on SMB export on AD unable to resolve user/group name; added version control
1.1n - Error handling on createNFS


syncisires.py Features
==============
To run:
```
OneFS#> ./syncisires.py -h
usage: syncisires.py [-h] {init,export,create,updatezonepath} ...

Sync SMB/NFS setting between 2 zones/clusters

positional arguments:
  {init,export,create,updatezonepath}
    init                Initialize the environment
    export              Export SMB/NFS setting from --source
    create              Import SMB/NFS setting from directory provided to
                        --target
    updatezonepath      To update the zone path in the JSON file in a
                        directory

optional arguments:
  -h, --help            show this help message and exit
OneFS#>

```

positional arguments:
init - Initialize the environment to default
```
OneFS#> ./syncisires.py init --help
usage: syncisires.py init [-h]

optional arguments:
  -h, --help  show this help message and exit
OneFS#>


Example:
========

OneFS#>  ./syncisires.py init
Cleaning up Env.....
OneFS#>  ls -l
total 16
-rw-r--r--     1 root  wheel  1150 Jun 21 01:01 nfs.keys
-r--r--r--     1 root  wheel  1081 Jun 17 16:01 smb.keys
drwxr-xr-x     2 root  wheel   512 Jun 21 12:05 src
-rwxr--r--     1 root  wheel  2578 Jun 21 11:46 syncisires.py
OneFS#>

```
positional arguments:
export - Initialize the environment to default
```
OneFS#> ./syncisires.py export --help
usage: syncisires.py export [-h] -s SOURCE -r RESOURCE [--id ID]

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        Please key in the source URL to export the SMB
  -r RESOURCE, --resource RESOURCE
                        SMB/NFS you want to export
  --id ID               Export Single Share
OneFS#>

Example:
========

OneFS#>  ./syncisires.py export --source localhost:8080 -r smb
Exporting smb from localhost:8080
Source zone username: root
Enter the Password:
Total: 2 share(s) exported in /ifs/data/Isilon_support/syncisires/JSON_SMB_localhost
OneFS#>   ls -lrt /ifs/data/Isilon_support/syncisires/JSON_SMB_localhost
total 12
-rw-r--r--     1 root  wheel  1594 Jun 21 13:29 share1.json
-rw-r--r--     1 root  wheel  1625 Jun 21 13:29 share2.json
OneFS#>

```

positional arguments:
Create - Import SMB/NFS setting from directory provided to --target
```
OneFS#> ./syncisires.py create --help
usage: syncisires.py create [-h] -d DIR -t TARGET -r RESOURCE

optional arguments:
  -h, --help            show this help message and exit
  -d DIR, --dir DIR     Directory of the JSON file to be created
  -t TARGET, --target TARGET
                        URL of the Target zone
  -r RESOURCE, --resource RESOURCE
                        Specifiy SMB/NFS you want to create
OneFS#>

Example:
========

OneFS#> ./syncisires.py create -d JSON_SMB_localhost -t localhost:8080 -r smb
Creating smb share at : localhost:8080 using JSON file(s) in : JSON_SMB_localhost
Target zone username: root
Enter the Password:
Share : share1 created on localhost:8080
Share : share2 created on localhost:8080
OneFS#>
========

```

positional arguments:
updatezonepath - To update the zone path in the JSON file in a directory
```
OneFS#> ./syncisires.py updatezonepath --help
usage: syncisires.py updatezonepath [-h] -d DIR -o OLDZONEPATH -n NEWZONEPATH

optional arguments:
  -h, --help            show this help message and exit
  -d DIR, --dir DIR     Directory of the JSON file to be updated
  -o OLDZONEPATH, --oldZonepath OLDZONEPATH
                        Input the old zone path
  -n NEWZONEPATH, --newZonepath NEWZONEPATH
                        Input the new zone path

OneFS#>

Example:
========
OneFS#>  grep ifs JSON_SMB_localhost/*.json
JSON_SMB_localhost/share1.json:    "path": "/ifs/share1",
JSON_SMB_localhost/share2.json:    "path": "/ifs/share2",
OneFS#> ./syncisires.py updatezonepath -d JSON_SMB_localhost -o /ifs -n /ifs/appsvol
Processing zonepath update on: JSON_SMB_localhost
swapping zone for: JSON_SMB_localhost/share1.json
Saving in :updated-JSON_SMB_localhost/updated-share1.json
swapping zone for: JSON_SMB_localhost/share2.json
Saving in :updated-JSON_SMB_localhost/updated-share2.json
OneFS#> grep ifs updated-JSON_SMB_localhost/*.json
updated-JSON_SMB_localhost/updated-share1.json:    "path": "/ifs/appsvol/share1",
updated-JSON_SMB_localhost/updated-share2.json:    "path": "/ifs/appsvol/data/Isilon_Support/share2",
OneFS#>
```
```
updatezonepath function will only change the path that you provided in the command
    oldzonepath = /ifs
    newzonepath = /ifs/appsvol

If you wish to change the path sturcture different from the oringial, put in another folder and run the command again:
From /ifs/appsvol/data/Isilon_Support/share2   change to /ifs/appsvol/share2

OneFS#> ./syncisires.py updatezonepath -d {new dir of updated-share2.json} -o /ifs/appsvol/data/Isilon_Support -n /ifs/appsvol
```

positional arguments:
version - To show the version
```
OneFS#>  ./syncisires.py version -h
usage: syncisires.py version [-h] [-d DETAILS]

optional arguments:
  -h, --help            show this help message and exit
  -d DETAILS, --details DETAILS
                        Display all src version: Type 'all'
						

OneFS#> ./syncisires.py version
syncisires.py   : 1.1
OneFS#> ./syncisires.py version  -d all
syncisires.py   : 1.1
Environment     : 1.0
ISI API call    : 1.1
Header          : 1.0
Export SMB      : 1.1
Export NFS      : 1.0
Create SMB      : 1.0
Create NFS      : 1.0
Update Zone Path: 1.0
OneFS#>

```


