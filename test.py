import re
import fileinput
import os
import sys
import string

ip = "1.1.1.1"

with open('net-script.bak', 'r') as file:
    filedata = file.read()
    print(filedata.replace("IPADDR=172.100.12.1", f"IPADDR={ip}"))
    