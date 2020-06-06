import os
import subprocess
from xml.dom import minidom
import fileinput
import re
import time


os.system('vmtoolsd --cmd "info-get guestinfo.ovfEnv" > sample.xml')
xmldoc = minidom.parse('sample.xml')
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

nname = "ens192"
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


if os.path.isfile('first-run'):
    pass
else:
    change_hostname(fqdn)
    replacer('/etc/sysconfig/network-scripts/ifcfg-ens192',
             'BOOTPROTO', "BOOTPROTO=static")
    replacer('/etc/sysconfig/network-scripts/ifcfg-ens192',
             "NETMASK=", f"NETMASK={netmask}")
    replacer('/etc/sysconfig/network-scripts/ifcfg-ens192',
             "IPADDR=", f"IPADDR={ipaddr}")
    replacer('/etc/sysconfig/network-scripts/ifcfg-ens192',
             'GATEWAY=', f"GATEWAY={gw}")
    replacer('/etc/sysconfig/network-scripts/ifcfg-ens192',
             'DNS1=', f"DNS1={dns}")
    subprocess.run(["touch", "first-run"])
    time.sleep(10)
    os.system("rm -rf sample.xm")
    os.system("shutdown -r now")
