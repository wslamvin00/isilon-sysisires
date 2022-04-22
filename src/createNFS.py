#!/usr/bin/python
import requests
import json
import sys
import headers as head
import isiapicall as isiapi
import env

requests.packages.urllib3.disable_warnings()
VERSION="1.1"

def createNFS(apiep,nfsdir):
    url=isiapi.genPOSTNFSAPIurl(apiep)
    exportlist=env.listjsonfile(nfsdir)
    headers = head.askTgtZonelogin()
    for nfs in exportlist:
	INPARA  = json.load(open(nfs))
	NFSPARA  = json.dumps(INPARA,sort_keys=True, indent=4, separators=(',', ': '))
    	try:
        	response = requests.post(url, verify=False ,headers=headers, data = NFSPARA )
        	response.raise_for_status()
    	except requests.exceptions.HTTPError as err:
            	headers=0
        	isiapi.APIerr(err.response.status_code)
		print("Error on Processing: " + nfs)
        	raise SystemExit(err)
	except requests.exceptions.ConnectionError as err:
            	headers=0
            	isiapi.APIerr(err.response.status_code)
            	print ("Please verify the Target address and port number")
            	raise SystemExit(err)

    	id=json.loads(response.content)
	exportid=str(id.get("id"))
    	print ("Export ID: "+exportid + " for file: "+nfs +" created on "+apiep )


if __name__ == '__main__':
    print("Please run syncisires")

