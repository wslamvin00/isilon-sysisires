import getpass
import sys
import base64
VERSION="1.0"

def convertBASIC(zone):
  if sys.version_info[0] < 3:
    user = raw_input(zone+" zone username: ") # (python 2.7)
  else:
    user = input(zone+" zone username: ")  # (python 3)
  p=getpass.getpass("Enter the Password: ")
  BASICPWD=user+":"+p
  p=0
  BASIC=base64.b64encode(BASICPWD.encode("utf-8"))
  return BASIC

def askSrcZonelogin():
  srcheaders = {'Authorization': 'Basic xxxxxxxxxxxxxxxxxxxx', 'Content-Type': 'application/json'}
  x=convertBASIC("Source")
  srcheaders.update({"Authorization": "Basic "+x})
  return srcheaders

def askTgtZonelogin():
  tgtheaders = {'Authorization': 'Basic xxxxxxxxxxxxxxxxxxxx', 'Content-Type': 'application/json'}
  x=convertBASIC("Target")
  tgtheaders.update({"Authorization": "Basic "+x})
  return tgtheaders

def convertRootBASIC(cluster):
  p=getpass.getpass("Please enter the root password for "+cluster+" : ")
  BASICPWD=user+":"+p
  p=0
  BASIC=base64.b64encode(BASICPWD.encode("utf-8"))
  return BASIC


if __name__ == '__main__':
    print("Please run syncisires")


