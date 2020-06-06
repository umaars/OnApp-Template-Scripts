from os import path
import subprocess
from xml.dom import minidom
import fileinput
import re


if path.exists("sample.xml"):
    print("True")
else:
    print("false")

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
    with open('net-script.bak', 'r') as file:
        filedata = file.read()
    print(filedata)
    filedata = filedata.replace('IPADDR=172.100.12.1', f'IPADDR={i}')
    filedata = filedata.replace('NETMASK=255.255.255.0', f'NETMASK={n}')
    filedata = filedata.replace('GATEWAY=172.0.0.1', f'GATEWAY={g}')
    filedata = filedata.replace('DNS1=172.100.12.1', f'DNS1={d}')

    with open('net-script.bak', 'w') as file:
        file.write(filedata)


change_hostname(fqdn)
set_net(ipaddr, netmask, gw, dns)
