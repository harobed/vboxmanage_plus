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
    p = subprocess.Popen(
        "VBoxManage list hdds",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, err = p.communicate()
    errcode = p.returncode

    for hdd in parse_vbox_manage_list_hdd(out):
        if hdd['state'] == 'inaccessible':
            remove_hdd(hdd['uuid'])

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

    orphaned_parser = remove_subparsers.add_parser("orphaned")
    orphaned_subparsers = orphaned_parser.add_subparsers(dest="orphaned_subparsers")

    hdds_parser = orphaned_subparsers.add_parser("hdds")

    args = root_parser.parse_args()

    if (
        (args.root_subparsers == 'remove') and
        (args.remove_subparsers == 'orphaned') and
        (args.orphaned_subparsers == 'hdds')
    ):
        remove_orphan_hdds()

if __name__ == '__main__':
    cli()
