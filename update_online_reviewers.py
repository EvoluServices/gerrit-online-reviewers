from pygerrit2.rest import GerritRestAPI
from requests.auth import HTTPDigestAuth
import os
import time
import online_devs

while True:
    auth = HTTPDigestAuth(os.getenv('GERRIT_USERNAME'), os.getenv('GERRIT_PASSWORD'))
    rest = GerritRestAPI(url=os.getenv('GERRIT_URL'), auth=auth)
    online_group = rest.get('/groups/')['online-reviewers']
    members = list(map(lambda x: x['_account_id'], rest.get('/groups/' + online_group['id'] + '/members/')))
    online_devs = online_devs.get_devs_online()
    print(online_devs)
    remove = list(filter(lambda x: x not in online_devs, members))
    add = list(filter(lambda x: x not in members, online_devs))
    for remove_id in remove:
        rest.delete('/groups/' + online_group['id'] + '/members/' + str(remove_id))
    for add_id in add:
        rest.put('/groups/' + online_group['id'] + '/members/' + str(add_id))
    time.sleep(900)
