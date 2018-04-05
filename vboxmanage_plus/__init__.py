import re
import subprocess
import argparse

__version__ = '0.1.0'

re_parse_vbox_manage_list_hdd = re.compile(
"""^UUID: *(?P<uuid>\S*?)$.*?
Parent UUID: *(?P<parent_uuid>.*?)$.*?
State: *(?P<state>.*?)$.*?
Location: *(?P<location>.*?)$.*?""",
    re.DOTALL|re.MULTILINE
)

def parse_vbox_manage_list_hdd(data):
    return [m.groupdict() for m in re_parse_vbox_manage_list_hdd.finditer(str(data))]


def remove_orphan_hdds():
    for hdd in list_orphan_hdds():
        remove_hdd(hdd['uuid'])


def list_orphan_hdds():
    p = subprocess.Popen(
        "VBoxManage list hdds",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, err = p.communicate()
    errcode = p.returncode

    return [
        hdd for hdd in parse_vbox_manage_list_hdd(out)
        if hdd['state'] == 'inaccessible'
    ]


def remove_rdd(uuid):
    print("Remove medium %s" % uuid)
    p = subprocess.Popen(
        "VBoxManage closemedium disk %s --delete" % uuid,
        shell=True
    )
    p.communicate()
    return p.returncode

def cli():
    root_parser = argparse.ArgumentParser()
    root_subparsers = root_parser.add_subparsers(dest="root_subparsers")

    remove_parser = root_subparsers.add_parser("remove")
    remove_subparsers = remove_parser.add_subparsers(dest="remove_subparsers")

    orphaned_remove_parser = remove_subparsers.add_parser("orphaned")
    orphaned_remove_subparsers = orphaned_remove_parser.add_subparsers(dest="orphaned_remove_subparsers")

    hdds_orphaned_remove_parser = orphaned_remove_subparsers.add_parser("hdds")

    list_parser = root_subparsers.add_parser("list")
    list_subparsers = list_parser.add_subparsers(dest="list_subparsers")

    orphaned_list_parser = list_subparsers.add_parser("orphaned")
    orphaned_list_subparsers = orphaned_list_parser.add_subparsers(dest="orphaned_list_subparsers")

    hdds_orphaned_list_parser = orphaned_list_subparsers.add_parser("hdds")

    args = root_parser.parse_args()
    print(args)

    if args.root_subparsers == 'list':
        if args.list_subparsers == 'orphaned':
            if args.orphaned_list_subparsers == 'hdds':
                for hdd in list_orphan_hdds():
                    print("%s - %s" % (hdd['uuid'], hdd['location']))

    elif args.root_subparsers == 'remove':
        if args.remove_subparsers == 'orphaned':
            if args.orphaned_remove_subparsers == 'hdds':
                remove_orphan_hdds()


if __name__ == '__main__':
    cli()
