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


def exportNFS(apiep,id):
        BASEDIR=env.BASEDIR
        TMP=env.TMPDIR
        URLobj=env.splitapiurl(apiep)
        NFSOUTDIR=env.createEnv(URLobj[0],"NFS")
        APIOUTPUT=os.path.join(TMP,URLobj[0]+"_getExport.out")
        headers = head.askSrcZonelogin()
        if not bool(id):
            url=isiapi.genNFSAPIURL(apiep,False,id)
        else:
            url=isiapi.genNFSAPIURL(apiep,True,id)
        try:
            response = requests.get(url, verify=False ,headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            headers=0
	    isiapi.APIerr(err.response.status_code)
            raise SystemExit(err)

        #headers=0
        open(APIOUTPUT, "w").write(
                json.dumps(response.json(), sort_keys=True, indent=4, separators=(',', ': '))
        )

        obj  = json.load(open(APIOUTPUT))
        ######### modify for NFS below
        exports=obj.get("exports")
        totalexport=obj.get("total")
        keydel = []
        with open("nfs.keys", "r") as a_file:
                for line in a_file:
                        stripped_line = line.strip()
                        if not stripped_line.startswith("#"):
                                keydel.append(stripped_line)
        newdir = []
        for x in range(len(exports)):
                #print (exports[x].get("id"))
                FILENAME=str(exports[x].get("id"))+".json"
                SAVEIN=os.path.join(NFSOUTDIR,FILENAME)
                tmppath=exports[x].get("paths")
                EXPORTPATH=tmppath[0]
		#print (EXPORTPATH)
		newdir.append(EXPORTPATH)
                for setting in keydel:
                        if setting in exports[x]:
                                del exports[x][setting]
                open(SAVEIN, "w").write(json.dumps(exports[x],sort_keys=True, indent=4, separators=(',', ': ')))

        print ("Total: " + str(len(exports)) + " NFS export(s) exported in " + NFSOUTDIR)
        print ("\n\nIsilon NFS do not auto create directory, please run the following ON THE TARGET CLUSTER before creating NFS\n\n")
        for tdir in range(len(newdir)):
            print ("#> mkdir -p "+newdir[tdir])



if __name__ == '__main__':
    print("Please run syncisires")



