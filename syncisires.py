#!/usr/bin/python

import argparse
import signal
import sys
import os
from src import env
from src import exportSMBinfo as getsmb
from src import exportNFSinfo as getnfs
from src import createSMB as crtsmb
from src import createNFS as crtnfs
from src import updateZonepath as upZonepath

VERSION = "1.1n"


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    print ("Removing " + env.TMPDIR)
    env.rmdirtree(env.TMPDIR)
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

parser = argparse.ArgumentParser(description='Sync SMB/NFS setting between 2 zones/clusters')
subparser = parser.add_subparsers(dest='command')

init = subparser.add_parser('init', help="Initialize the environment")
export = subparser.add_parser('export', help="Export SMB/NFS setting from --source")
create = subparser.add_parser('create', help="Import SMB/NFS setting from directory provided to --target")
updatezonepath = subparser.add_parser('updatezonepath', help="To update the zone path in the JSON file in a directory")
ver = subparser.add_parser('version', help="Display version")

export.add_argument('-s', '--source', type=str, required=True, help="Please key in the source URL to export the SMB")
export.add_argument('-r', '--resource', type=str, required=True, help="SMB/NFS you want to export")
export.add_argument('--id', type=str, required=False, help="Export Single Share")
create.add_argument('-d', '--dir', type=str, required=True, help="Directory of the JSON file to be created")
create.add_argument('-t', '--target', type=str, required=True, help="URL of the Target zone")
create.add_argument('-r', '--resource', type=str, required=True, help="Specifiy SMB/NFS you want to create")
updatezonepath.add_argument('-d', '--dir', type=str, required=True, help="Directory of the JSON file to be updated")
updatezonepath.add_argument('-o', '--oldZonepath', type=str, required=True, help="Input the old zone path")
updatezonepath.add_argument('-n', '--newZonepath', type=str, required=True, help="Input the new zone path")
ver.add_argument('-d', '--details', type=str, required=False, help="Display all src version: Type 'all'")

args = parser.parse_args()

if args.command == 'init':
    env.cleanup()
elif args.command == 'export':
    print("Exporting " + args.resource + " from " + args.source)
    type = args.resource
    if type.upper() == 'SMB':
        getsmb.exportSMB(args.source, args.id)
    elif type.upper() == 'NFS':
        getnfs.exportNFS(args.source, args.id)
    else:
        print("invalid resource\nExiting.....")
        exit(0)
elif args.command == 'create':
    type = args.resource
    print("Creating " + type + " share at : " + args.target + " using JSON file(s) in : " + args.dir)
    if type.upper() == 'SMB':
        crtsmb.createSMB(args.target, args.dir)
    elif type.upper() == 'NFS':
        crtnfs.createNFS(args.target, args.dir)
elif args.command == 'updatezonepath':
    upZonepath.updatezonepath(args.dir, args.oldZonepath, args.newZonepath)
elif args.command == 'version':
    print (os.path.basename(__file__) + "\t: " + VERSION)
    try:
        details = args.details
        details = details.upper()
        
        if details.startswith('A'):
            from src import isiapicall as isiapi
            from src import headers as head
    
            print ("Environment\t: " + env.VERSION)
            print ("ISI API call\t: " + isiapi.VERSION)
            print ("Header\t\t: " + head.VERSION)
            print ("Export SMB\t: " + getsmb.VERSION)
            print ("Export NFS\t: " + getnfs.VERSION)
            print ("Create SMB\t: " + crtsmb.VERSION)
            print ("Create NFS\t: " + crtnfs.VERSION)
            print ("Update Zone Path: " + upZonepath.VERSION)
    except:
        pass

else:
    print ("Invalid option")

