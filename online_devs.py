from nmap import PortScanner
import os

mac_dev_file = os.getenv('REVIEWERS_MAC_ADDRESS')
devs = {dev.split(' ')[0]: dev.split(' ')[1] for dev in mac_dev_file.split(';')}
ps = PortScanner()

def is_dev(ip):
    mac = ps[ip]['addresses'].get('mac', 'SEM MAC')
    print ps[ip]
    return mac in devs


def get_dev_id(ip):
    return int(devs[ps[ip]['addresses']['mac']])


def get_devs_online():
    ps.scan(hosts='192.168.0.*', arguments='-sP')
    dev_ids = map(get_dev_id, list(filter(is_dev, ps.all_hosts())))
    return list(set(dev_ids))

