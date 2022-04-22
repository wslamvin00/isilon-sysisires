import os
import env
import json
VERSION="1.1"

newdir = []

def swapzone(oldzone, newzone, obj):
    global newdir
    try:
        isSMB = False
        objPath = obj.get("paths")
        fullpath = str(objPath[0])
    except:
        isSMB = True
        objPath = obj.get("path")
        fullpath = objPath

    relative_path =  os.path.relpath(str(fullpath), oldzone)
    newpath=os.path.join(newzone,relative_path)
    if bool(isSMB):
      obj["path"] = newpath
    else:
      pathlist=[]
      pathlist.append(str(newpath))
      obj["paths"] = pathlist
      newdir.append(newpath)
    return obj

def getNFSFilelist(dir):
    nfsjsonfiles=env.listjsonfile(dir)
    return nfsjsonfiles

def updatezonepath(jsondir, oldzone, newzone):
    global newdir
    newdir=[]
    print ("Processing zonepath update on: "+jsondir)
    Jlist=env.listjsonfile(jsondir)
    if bool(env.checkemptylist(Jlist)):
        print ("There are no Json file found in : " + jsondir)
        exit(1)
    parentDir=os.path.split(jsondir)
    baseDir=os.path.basename(jsondir)
    outDir="updated-"+baseDir
    outputDir=os.path.join(parentDir[0],outDir)
    env.makedir(outputDir)
    for JFile in range(len(Jlist)):
        obj = json.load(open(Jlist[JFile]))
        newfilename = "updated-" + os.path.basename(Jlist[JFile])
        print ("swapping zone for: " + Jlist[JFile])
        updatedfile = swapzone(oldzone, newzone, obj)
        SAVEIN=os.path.join(outputDir,newfilename)
        print ("Saving in :"+SAVEIN)
        env.saveJson(updatedfile,SAVEIN)
    if not len(newdir) == 0:
    	print ("\nIsilon NFS do not auto create directory, please run the following ON THE TARGET CLUSTER before creating NFS\n\n")
	for dir in range(len(newdir)):
	  print ("#> mkdir -p " + str(newdir[dir]))


if __name__ == '__main__':
    print("Please run in syncisires")




