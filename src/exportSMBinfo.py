#!/usr/bin/python
import requests
import env
import headers as head
import sys
import os
import isiapicall as isiapi
import json
import fileinput

requests.packages.urllib3.disable_warnings()
VERSION="1.1"

def exportSMB(apiep,id):
        BASEDIR=env.BASEDIR
        TMP=env.TMPDIR
        URLobj=env.splitapiurl(apiep)
        SMBOUTDIR=env.createEnv(URLobj[0],"SMB")
        APIOUTPUT=os.path.join(TMP,URLobj[0]+"_getShare.out")
        headers = head.askSrcZonelogin()
        if not bool(id):
            url=isiapi.genSMBAPIurl(apiep,False,id)
        else:
            url=isiapi.genSMBAPIurl(apiep,True,id)
        try:
            response = requests.get(url, verify=False ,headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            headers=0
            isiapi.APIerr(err.response.status_code)
            raise SystemExit(err)
        except requests.exceptions.ConnectionError as err:
            headers=0
            isiapi.APIerr(err.response.status_code)
            print ("Please verify the Source address and port number")
            raise SystemExit(err)

        open(APIOUTPUT, "w").write(
                json.dumps(response.json(), sort_keys=True, indent=4, separators=(',', ': '))
        )

        obj  = json.load(open(APIOUTPUT))
        shares=obj.get("shares")
        SHARESID=[]
        keydel = []
        with open("smb.keys", "r") as a_file:
                for line in a_file:
                        stripped_line = line.strip()
                        if not stripped_line.startswith("#"):
                                keydel.append(stripped_line)


        for x in range(len(shares)):
                #SHARESID.append(shares[x].get("id"))
                FILENAME=shares[x].get("id")+".json"
                SAVEIN=os.path.join(SMBOUTDIR,FILENAME)
                shares[x].update({"auto_create_directory":"true"})
                for setting in keydel:
                        if setting in shares[x]:
                                del shares[x][setting]
                for setting in shares[x]["run_as_root"]:
                        if "name" in setting:
                                del setting["name"]
                        if "type" in setting:
                                del setting["type"]
                try:
                    for perm in shares[x]["permissions"]:
                        del perm["trustee"]["name"]
                        del perm["trustee"]["type"]
                except:
                   pass 
                    
                open(SAVEIN, "w").write(json.dumps(shares[x],sort_keys=True, indent=4, separators=(',', ': ')))
                for line in fileinput.input(SAVEIN, inplace=True):
                        print line.replace("\"auto_create_directory\": \"true\",", "\"auto_create_directory\": true,"),
        print ("Total: " + str(len(shares)) + " share(s) exported in " + SMBOUTDIR)

if __name__ == '__main__':
    print("Please run syncisires")


