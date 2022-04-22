#!/usr/bin/python
import requests
import json
import sys
import headers as head
import isiapicall as isiapi
import env

requests.packages.urllib3.disable_warnings()
VERSION="1.1"


def createSMB(apiep,smbdir):
    url=isiapi.genPOSTSMBAPIurl(apiep)
    sharelist=env.listjsonfile(smbdir)
    headers = head.askTgtZonelogin()
    for smb in sharelist:
	INPARA  = json.load(open(smb))
	SMBPARA  = json.dumps(INPARA,sort_keys=True, indent=4, separators=(',', ': '))
    	try:
        	response = requests.post(url, verify=False ,headers=headers, data = SMBPARA )
        	response.raise_for_status()
    	except requests.exceptions.HTTPError as err:
		headers=0
        	isiapi.APIerr(err.response.status_code)
		print("Error on Processing: " + smb)
        	raise SystemExit(err)
	except requests.exceptions.ConnectionError as err:
            headers=0
            isiapi.APIerr(err.response.status_code)
            print ("Please verify the Source address and port number")
            raise SystemExit(err)

    	id=json.loads(response.content)
	shareid=str(id.get("id"))
    	print ("Share : "+shareid +" from file: "+smb+ " created on "+apiep )


if __name__ == '__main__':
    print("Please run syncisires")

