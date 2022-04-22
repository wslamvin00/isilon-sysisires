SMBAPIVER="7"
NFSAPIVER="4"
QUOTAAPIVER="8"
VERSION="1.2"

def genSMBAPIurl(APIEP,SINGLE,ID):
    global SMBAPIVER
    if not SINGLE:
        url = "https://{}/platform/{}/protocols/smb/shares".format(APIEP,SMBAPIVER)
    else:
        url = "https://{}/platform/{}/protocols/smb/shares/{}".format(APIEP,SMBAPIVER,ID)
    return url

def genNFSAPIURL(APIEP,SINGLE,ID):
    global NFSAPIVER
    if not SINGLE:
        url = "https://{}/platform/{}/protocols/nfs/exports".format(APIEP,NFSAPIVER)
    else:
        url = "https://{}/platform/{}/protocols/nfs/exports/{}".format(APIEP,NFSAPIVER,ID)
    return url

def genPOSTSMBAPIurl(APIEP):
    global SMBAPIVER
    url = "https://{}/platform/{}/protocols/smb/shares".format(APIEP,SMBAPIVER)
    return url

def genPOSTNFSAPIurl(APIEP):
    global NFSAPIVER
    url = "https://{}/platform/{}/protocols/nfs/exports".format(APIEP,NFSAPIVER)
    return url

def genPOSTQUOTAAPIurl(APIEP):
    global QUOTAAPIVER
    url = "https://{}/platform/{}/quota/quotas".format(APIEP,QUOTAAPIVER)
    return url
    
def genPOSTQNOTIFYAAPIurl(APIEP, QID):
    global QUOTAAPIVER
    url = "https://{}/platform/{}/quota/quotas/{}/notifications".format(APIEP,QUOTAAPIVER,QID)
    return url    
    
def APIerr(err):
    if err == 409:
        print("Resource Exist!!!")
    elif err == 401:
        print ("Login Err (Unauthorized): please check do you have zone admin access!!")
    elif err == 500:
        print ("Interal Server error on Isilon, Please process this request manaully to identify the error")
	print ("Possible cause: ")
	print ("- Error when creating NFS: directory is not created")

def genSEARCHQUOTA(APIEP,PATH):
    global QUOTAAPIVER
    url = "https://{}/platform/{}/quota/quotas?path={}".format(APIEP,QUOTAAPIVER,PATH)
    return url

def genSEARCHQUOTANOTIFY(APIEP,QID):
    global QUOTAAPIVER
    url = "https://{}/platform/{}/quota/quotas/{}/notifications".format(APIEP,QUOTAAPIVER,QID)
    return url



if __name__ == '__main__':
    print("Please run syncisires")


