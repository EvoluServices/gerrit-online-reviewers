from nmap import PortScanner
import csv
import requests
import os

ps = PortScanner()

def is_dev(ip, devs):
    mac = ps[ip]['addresses'].get('mac', 'SEM MAC')
    return mac in devs


def get_dev_id(ip, devs):
    return int(devs[ps[ip]['addresses']['mac']])


def get_devs_online():
    ps.scan(hosts='192.168.0.*', arguments='-sP')
    url = os.getenv('REVIEWERS_URL')
    response = requests.get(url)
    data = response.content
    reader = csv.reader(data.splitlines(), delimiter=',')

    devs = {dev[2]: dev[1] for dev in list(reader)}
    dev_ids = map(lambda x: get_dev_id(x, devs), list(filter(lambda x: is_dev(x, devs), ps.all_hosts())))
    return list(set(dev_ids))

