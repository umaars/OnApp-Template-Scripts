#!/usr/bin/env python3

from xml.dom import minidom
import os
import subprocess
import fileinput
import shlex
import time
import logging


# Added Logging

logname = "log.txt"
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(levelname)s %(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


def xmlparser():
    '''
    Parses a vmware tools XML file and returns all properties in a dictionary
    '''
    # with open('sample.xml', 'w') as f:
    #     p1 = subprocess.run(
    #         'vmtoolsd --cmd "info-get guestinfo.ovfEnv" >> sample.xml', stdout=f, shell=True)
    #     f.close()
    PROPERTIES = {}
    p = minidom.parse('sample.xml')
    item_list = p.getElementsByTagName('Property')
    for i in item_list:
        key = i.attributes['oe:key'].value
        value = i.attributes['oe:value'].value
        PROPERTIES[key] = value
    return PROPERTIES


def createNetworkProps(parsed_xml):
    network_props = {
        'BOOTPROTO': "BOOTPROTO=static",
        "NETMASK=": f"NETMASK={properties['onapp.netmask']}",
        "IPADDR=": f"IPADDR={properties['onapp.ipaddr']}",
        'GATEWAY=': f"GATEWAY={properties['onapp.gw']}",
        'DNS1=': f'DNS1={properties["onapp.dns"]}',
    }

    return network_props

def createOnAppProps(parsed_xml):
    onapp_props = {
        'license_key' : f'{parsed_xml["onapp.license"]}'
    }
    return onapp_props


def changer(props,file_to_change):
    """Function to update files in place

    Arguments:
        props {Dictionary} -- Dictionary where key = lookup line string and value = new line value
        file_to_change {Filename} -- Filename to make changes
        Does not output anything , changes are made inside the file
    """

    mylist = list(props.keys())
    for line in fileinput.input(files=(file_to_change), inplace=1):
        for each in mylist:
            if each in line:
                line = f"{props[each]}\n"
            else:
                line = line
        print(line, end='')


properties = xmlparser()
print(properties)
logging.info(properties)
net_props = createNetworkProps(properties)
logging.info(net_props)
onapp_props = createOnAppProps(properties)
logging.info(onapp_props)

logging.info(f"Setting hostname to {properties['onapp.fqdn']} ")
hname_cmd = f"hostnamectl set-hostname {properties['onapp.fqdn']}"
hname_cmd = shlex.split(hname_cmd)
print(hname_cmd)
hname_set = subprocess.Popen(hname_cmd)
hname_set.wait()
print("finished")
os.system(f"export HOSTNAME={properties['onapp.fqdn']}")
print(f"export HOSTNAME={properties['onapp.fqdn']}")
time.sleep(1)
os.system("service rabbitmq-server restart")
rabbitmq_cmd = shlex.split("/onapp/onapp-rabbitmq/onapp-cp-rabbitmq.sh")
reinstall_rabbitmq = subprocess.Popen(rabbitmq_cmd,shell=True)
reinstall_rabbitmq.wait()
print("reinstalled_rabbitmq")

# Sample Dictionary to change values in Centos 7 network scripts file for interface ens160
# "/etc/sysconfig/network-scripts/ifcfg-ens160"
#    my_pattern = {
#     'BOOTPROTO': "BOOTPROTO=static",
#     "NETMASK=": f"NETMASK={data_dict['onapp.netmask']}",
#     "IPADDR=": f"IPADDR={data_dict['onapp.ipaddr']}",
#     'GATEWAY=': f"GATEWAY={data_dict['onapp.gw']}",
#     'DNS1=': f'DNS1={data_dict["onapp.dns"]}',
# }


# if os.path.isfile('/root/first-run'):
#     os.system('echo "`date` Not RUN" >> /root/first-run')
#     os.system('echo "`date` ONAPP TEMPLATE SCRIPT FAILED" | tee /dev/kmsg')
#     logging.info("Aborting: first-run file exists!")
# else:
#     print("Parsing OVF Properties")
#     logging.info("Parsing OVF Properties")
#     properties = xmlparser()
#     time.sleep(2)
#     print("Changing Hostname")
#     logging.info("Changin Hostname")
#     changeHostname = os.system(
#         f"nmcli general hostname {properties['onapp.fqdn']}")
#     time.sleep(2)
#     print("Updating Network Settings")
#     logging.info("Changing Hostname")
#     changer("/etc/sysconfig/network-scripts/ifcfg-ens160")
#     time.sleep(2)
#     logging.info(
#         "Creating first run file to abort script execution in future!")
#     os.system("touch /root/first-run")
#     print("Restarting Network")
#     logging.info("Restarting Network")
#     os.system("systemctl restart network")
#     time.sleep(2)
#     logging.info("Updating OnApp installer")
#     cmd = "yum -y update onapp-cp-install"
#     newcmd = shlex.split(cmd)
#     p1 = subprocess.run(newcmd, stdout=subprocess.PIPE,
#                         universal_newlines=True)
#     print(p1.stdout)
#     os.system('echo "`date` RUN" >> /root/first-run')
#     os.system('echo "`date` ONAPP TEMPLATE SCRIPT" | tee /dev/kmsg')
#     logging.info("Script Execution finished. Restarting System")
#     # os.system("systemctl reboot")
