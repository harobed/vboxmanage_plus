__version__ = '0.1.0'
import re

re_parse_vbox_manage_list_hdd = re.compile(
"""^UUID: *(?P<uuid>\S*?)$.*?
Parent UUID: *(?P<parent_uuid>.*?)$.*?
State: *(?P<state>.*?)$.*?
Location: *(?P<location>.*?)$.*?""",
    re.DOTALL|re.MULTILINE
)

def parse_vbox_manage_list_hdd(data):
    return [m.groupdict() for m in re_parse_vbox_manage_list_hdd.finditer(data)]
