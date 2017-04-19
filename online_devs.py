from nmap import PortScanner

with open('macaddress-names') as mac_dev_file:
    devs = {dev.split(' ')[0]: dev.split(' ')[1] for dev in mac_dev_file.readlines()}
ps = PortScanner()


def is_dev(ip):
    mac = ps[ip]['addresses'].get('mac', 'SEM MAC')
    return mac in devs


def get_dev_id(ip):
    return int(devs[ps[ip]['addresses']['mac']])


def get_devs_online():
    ps.scan(hosts='192.168.0.*', arguments='-sP -PA21,23,80,3389')
    dev_ids = map(get_dev_id, list(filter(is_dev, ps.all_hosts())))
    return list(set(dev_ids))

