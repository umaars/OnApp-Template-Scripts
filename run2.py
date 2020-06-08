from xml.dom import minidom
import os
import subprocess
import fileinput


def xmlparser():
    '''
    Parses a vmware tools XML file and returns all properties
    '''
    with open('sample.xml', 'w') as f:
        p1 = subprocess.run(
            'vmtoolsd --cmd "info-get guestinfo.ovfEnv" >> sample.xml', stdout=f, shell=True)
        f.close()
    PROPERTIES = {}
    p = minidom.parse('sample.xml')
    item_list = p.getElementsByTagName('Property')
    for i in item_list:
        key = i.attributes['oe:key'].value
        value = i.attributes['oe:value'].value
        PROPERTIES[key] = value
    return PROPERTIES


nname = "/etc/sysconfig/network-scripts/ifcfg-ens160"


def changeNetworkOptions(data_dict, nname):
    my_pattern = {
        'BOOTPROTO': "BOOTPROTO=static",
        "NETMASK=": f"NETMASK={data_dict['onapp.netmask']}",
        "IPADDR=": f"IPADDR={data_dict['onapp.ipaddr']}",
        'GATEWAY=': f"GATEWAY={data_dict['onapp.gw']}",
        'DNS1=': f'DNS1={data_dict["onapp.dns"]}',
    }
    for line in fileinput(files=(nname), inplace=1):
        mylist = list(my_pattern.keys())
        for each in mylist:
            if each in line:
                line = f"{my_pattern[each]}\n"
            else:
                line = line
        return line


ovf_options = xmlparser()
print(xmlparser())
