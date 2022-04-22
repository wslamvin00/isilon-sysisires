import os
import sys
from glob import glob
from shutil import rmtree
import shutil
import glob as glob2
import json

BASEDIR=os.getcwd()
TMPDIR=os.path.join(BASEDIR, "tmp")
#SUCCESSEDJSON=os.path.join(BASEDIR, "Success")
#DLQ=os.path.join(BASEDIR, "ErrJsonQ")
VERSION="1.0"

def makedir(inpath):
    if not os.path.exists(inpath):
      os.makedirs(inpath)

def genAPIDir(apiep,restype):
  global BASEDIR
  folder="JSON" + "_"+ restype.upper()+"_" + apiep
  GETRESDIR=os.path.join(BASEDIR,folder)
  makedir(GETRESDIR)
  return GETRESDIR

def createEnv(apiep,restype):
  makedir(TMPDIR)
  return (genAPIDir(apiep,restype))

def rmdirtree(pattern):
    try:
        for item in glob(pattern):
          if not os.path.isdir(item):
            continue
          rmtree(item)
    except OSError as e:
        print("Error: %s : %s" % (file_path, e.strerror))

def cleanup():
    JSONFOLDER = os.path.join(BASEDIR, "JSON*")
    print("Cleaning up Env.....")
    rmdirtree(JSONFOLDER)
    JSONFOLDER = os.path.join(BASEDIR, "updated-JSON*")
    rmdirtree(JSONFOLDER)
    rmdirtree(TMPDIR)

def ask_yesno(prompt):
    if sys.version_info[0] < 3:
        yesno = raw_input(prompt) # (python 2.7)
    else:
        yesno = input(prompt)  # (python 3)

    if yesno.upper() == "Y":
        return True
    elif yesno.upper() == "N":
        return False
    else:
        print("Invalid input!")
        return False

def splitapiurl(apiep):
    urlsplit = apiep.split(":")
    return urlsplit

def isfexist(file):
    if os.path.isfile(file):
        return True
    else:
        return False

def isDexist(path):
    if os.path.isdir(path):
        return True
    else:
        return False

def listf(path):
    file_list=os.listdir(path)
    for i in range(len(file_list)):
        print (file_list[i])
    return file_list

def listjsonfile(path):
        JSONFPATH=os.path.join(path,"*.json")
        jfile=glob2.glob(JSONFPATH)
        return jfile

def ask_input(prompt):
    if sys.version_info[0] < 3:
        userinput = raw_input(prompt) # (python 2.7)
    else:
        userinput = input(prompt)  # (python 3)
    return userinput

def saveJson(jsonobj, SAVEIN):
    open(SAVEIN, "w").write(json.dumps(jsonobj,
                            sort_keys=True, indent=4, separators=(',', ': ')))

def checkemptylist(inlist):
    if len(inlist) == 0:
        return True
    else:
        return False

if __name__ == '__main__':
    print("Please run syncisires")

