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

fqdn = ''
ipaddr = ''
netmask = ''
gw = ''
dns = ''

for i in itemlist:
    a = {}
    key = i.attributes['oe:key'].value
    value = i.attributes['oe:value'].value
    if key == 'onapp.gw':
        gw = value
    if key == 'onapp.fqdn':
        fqdn = value
    if key == 'onapp.ipaddr':
        ipaddr = value
    if key == 'onapp.dns':
        dns = value
    if key == 'onapp.netmask':
        netmask = value

print(f"{fqdn} {ipaddr} {netmask} {gw} {dns}")


def change_hostname(hname):
    print(f"Setting new hostname: {hname}")
    os.system(f"nmcli general hostname {hname}")


def replacer(file, pattern, replace):
    x = fileinput.input(files=file, inplace=1)
    for line in x:
        if pattern in line:
            line = f"{replace}\n"
        print(line, end='')
    x.close()


nname = "ens160"
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
    replacer(f'/etc/sysconfig/network-scripts/ifcfg-{nname}',
             'BOOTPROTO', "BOOTPROTO=static")
    replacer(f'/etc/sysconfig/network-scripts/ifcfg-{nname}',
             "NETMASK=", f"NETMASK={netmask}")
    replacer(f'/etc/sysconfig/network-scripts/ifcfg-{nname}',
             "IPADDR=", f"IPADDR={ipaddr}")
    replacer(f'/etc/sysconfig/network-scripts/ifcfg-{nname}',
             'GATEWAY=', f"GATEWAY={gw}")
    replacer(f'/etc/sysconfig/network-scripts/ifcfg-{nname}',
             'DNS1=', f"DNS1={dns}")
    print("NEWORK UPDATED")
    logging.info("Network config updated")
    subprocess.run(["touch", "/root/scripts/OnApp-Template-Scripts/first-run"])
    time.sleep(10)
    logging.info("Sleeping Before Reboot")
    os.system("rm -rf /root/scripts/OnApp-Template-Scripts/sample.xml")
    # print("Rebooting Now!!!!")
    os.system("shutdown -r now")
