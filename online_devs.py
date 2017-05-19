from nmap import PortScanner
import csv
import requests
import os

url = os.getenv('REVIEWERS_URL')
response = requests.get(url)
data = response.content
reader = csv.reader(data.splitlines(), delimiter=',')

devs = {dev[2]: dev[1] for dev in list(reader)}
ps = PortScanner()

def is_dev(ip):
    mac = ps[ip]['addresses'].get('mac', 'SEM MAC')
    return mac in devs


def get_dev_id(ip):
    return int(devs[ps[ip]['addresses']['mac']])


def get_devs_online():
    ps.scan(hosts='192.168.0.*', arguments='-sP')
    dev_ids = map(get_dev_id, list(filter(is_dev, ps.all_hosts())))
    return list(set(dev_ids))

