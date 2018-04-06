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
    return [m.groupdict() for m in re_parse_vbox_manage_list_hdd.finditer(data.decode('utf8'))]


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


def remove_hdd(uuid):
    print("Remove medium %s" % uuid)
    p = subprocess.Popen(
        "VBoxManage closemedium disk %s --delete" % uuid,
        shell=True
    )
    p.communicate()
    return p.returncode


def parse_vbox_manage_list_vms(data):
    if data.decode("utf8").strip() == '':
        return []

    return [
        {
            "uuid": item.split(" ")[1].lstrip('{').rstrip('}')
        }
        for item in data.decode("utf8").strip().split("\n")
    ]

def list_vms():
    p = subprocess.Popen(
        "VBoxManage list vms",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, err = p.communicate()
    errcode = p.returncode

    return parse_vbox_manage_list_vms(out)


def destroy_vms(uuid):
    print("Destroy vms %s" % uuid)
    p = subprocess.Popen(
        "vboxmanage controlvm %s poweroff" % uuid,
        shell=True
    )
    p.communicate()
    p = subprocess.Popen(
        "vboxmanage unregistervm %s --delete" % uuid,
        shell=True
    )
    p.communicate()


def remove_vms():
    for vms in list_vms():
        destroy_vms(vms['uuid'])

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

    vms_remove_parser = remove_subparsers.add_parser("vms")
    vms_remove_subparsers = vms_remove_parser.add_subparsers(dest="vms_remove_subparsers")

    vms_list_parser = list_subparsers.add_parser("vms")
    vms_list_subparsers = vms_list_parser.add_subparsers(dest="vms_list_subparsers")

    args = root_parser.parse_args()

    if args.root_subparsers == 'list':
        if args.list_subparsers == 'orphaned':
            if args.orphaned_list_subparsers == 'hdds':
                for hdd in list_orphan_hdds():
                    print("%s - %s" % (hdd['uuid'], hdd['location']))
        elif args.list_subparsers == 'vms':
            for vms in list_vms():
                print("%s" % vms['uuid'])


    elif args.root_subparsers == 'remove':
        if args.remove_subparsers == 'orphaned':
            if args.orphaned_remove_subparsers == 'hdds':
                for hdd in list_orphan_hdds():
                    print("Remove %s - %s" % (hdd['uuid'], hdd['location']))
                    remove_hdd(hdd['uuid'])
        elif args.remove_subparsers == 'vms':
            remove_vms()


if __name__ == '__main__':
    cli()
