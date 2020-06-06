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
    run = subprocess.run(["hostnamectl", "set-hostname",
                          hname], shell=True, check=True)


def set_net(i, n, g, d):
    print(f"Setting Network Configs")
    with open('/etc/sysconfig/network-scripts/ifcfg-ens192', 'r') as file:
        filedata = file.read()
    print(filedata)
    filedata = filedata.replace('BOOTPROTO=dhcp', "BOOTPROTO=static")
    filedata = filedata.replace('IPADDR=10.200.1.100', f'IPADDR={i}')
    filedata = filedata.replace('NETMASK=255.255.255.0', f'NETMASK={n}')
    filedata = filedata.replace('GATEWAY=10.200.1.1', f'GATEWAY={g}')
    filedata = filedata.replace('DNS1=1.1.1.1', f'DNS1={d}')

    with open('/etc/sysconfig/network-scripts/ifcfg-ens192', 'w') as file:
        file.write(filedata)

    return (f" Set : {fqdn} {ipaddr} {netmask} {gw} {dns}")


if os.path.isfile('first-run'):
    pass
else:
    change_hostname(fqdn)
    set_net(ipaddr, netmask, gw, dns)
    subprocess.run(["touch", "first-run"])
    time.sleep(10)
    os.system("rm -rf sample.xm")
    os.system("shutdown -r now")
