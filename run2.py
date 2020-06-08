from xml.dom import minidom
import os
import subprocess

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


ovf_options = xmlparser()

def changeNetworkOptions(data_dict):
    my_pattern = {
        'BOOTPROTO': "BOOTPROTO=static",
        "NETMASK=": f"NETMASK={data_dict['onapp.netmask']}",
        "IPADDR=": f"IPADDR={data_dict['onapp.ipaddr']}",
        'GATEWAY=': f"GATEWAY={data_dict['onapp.gw']}",
        'DNS1=': f'DNS1={data_dict["onapp.dns"]}',
    }


print(xmlparser())
