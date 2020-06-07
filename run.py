import os
import subprocess
from xml.dom import minidom
import fileinput
import re
import time
import logging

logging.basicConfig(filename='/root/scripts/OnApp-Template-Scripts/log.txt',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)


os.system('vmtoolsd --cmd "info-get guestinfo.ovfEnv" > /root/scripts/OnApp-Template-Scripts/sample.xml')
xmldoc = minidom.parse('/root/scripts/OnApp-Template-Scripts/sample.xml')
itemlist = xmldoc.getElementsByTagName('Property')


PROPERTIES = {}
for i in itemlist:

    key = i.attributes['oe:key'].value
    value = i.attributes['oe:value'].value
    PROPERTIES[key] = value


print(PROPERTIES)

patterns = {'BOOTPROTO': "BOOTPROTO=static", "NETMASK=": f"NETMASK={PROPERTIES['onapp.netmask']}",
            "IPADDR=": f"IPADDR={PROPERTIES['onapp.ipaddr']}", 'GATEWAY=': f"GATEWAY={PROPERTIES['onapp.gw']}", 'DNS1=': f'DNS1={PROPERTIES["onapp.dns"]}', }
print(patterns)


def change_hostname(hname):
    print(f"Setting new hostname: {hname}")
    os.system(f"nmcli general hostname {hname}")


def replace(mydict, line):
    mylist = list(mydict.keys())
    for each in mylist:
        if each in line:
            line = f"{mydict[each]}\n"
        else:
            line = line
    return line


nname = "/etc/sysconfig/network-scripts/ifcfg-ens160"

if os.path.isfile('/root/scripts/OnApp-Template-Scripts/first-run'):
    logging.info("first-run exists. Exiting!")
    quit()
else:
    logging.info(f"changing hostname to {fqdn}")
    change_hostname(fqdn)
    print("UPDATING Network Config")
    logging.info(
        f"Setting IP: {ipaddr}, Subnet Mask: {netmask}, Gateway: {gw}, DNS: {dns}")
    logging.info("UPDATING Network Config")
    for line in fileinput.input(files=(nname), inplace=1):
        line = replace(patterns, line)
        print(line, end='')

    print("NEWORK UPDATED")
    logging.info("Network config updated")
    subprocess.run(["touch", "/root/scripts/OnApp-Template-Scripts/first-run"])
    time.sleep(10)
    logging.info("Sleeping Before Reboot")
    os.system("rm -rf /root/scripts/OnApp-Template-Scripts/sample.xml")
    # print("Rebooting Now!!!!")
    os.system("shutdown -r now")
