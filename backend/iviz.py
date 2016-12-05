import urllib2
import json
import threading
from collections import OrderedDict

seen=set()


def get_response_json_object(url, max):

    auth_token="Token token=f0fc702567df451dc5c346b98881eaea"
    req=urllib2.Request(url, None, {"Authorization":auth_token,"Content-type":'application/json'})
    print req
    response=urllib2.urlopen(req)
    html=response.read()
    json_obj=json.loads(html)
    tempMax = 0
    for d in json_obj:
        oid=d["id"]
        if oid <= max:
            break
        if oid > tempMax:
            tempMax = oid
        print oid
        if oid not in seen:
            seen.add(oid)
            with open('data.txt', 'a') as outfile:
                json.dump(d, outfile, sort_keys = True, indent = 4,
                ensure_ascii=False)
    if tempMax < max:
        tempMax = max
    threading.Timer(180, get_response_json_object(url,tempMax)).start()

get_response_json_object("http://feed.accern.com/v3/alphas", 0)
