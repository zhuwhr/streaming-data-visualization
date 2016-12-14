import urllib2
import json
import threading

import time

from Backend.app import es,socketio,app
from requests import post


def get_response_json_object(url, max):

    auth_token = "Token token=f0fc702567df451dc5c346b98881eaea"
    while True:

        req=urllib2.Request(url, None, {"Authorization":auth_token,"Content-type":'application/json'})
        print req
        response=urllib2.urlopen(req)
        html=response.read()
        json_obj=json.loads(html)
        for d in json_obj:
            oid=d["id"]
            if oid <= max:
                break
            else:
                max = oid
            print oid
            post('http://localhost:5000/api/article', json=d)
        time.sleep(0.18)


re = es.search(index='articles', doc_type='article', body={"aggs": {"max_id": {"max": {"field": "id"}}}}, size=1)
max_id = re['aggregations']['max_id']['value']
print(max_id)
threading.Timer(180, get_response_json_object("http://feed.accern.com/v3/alphas", max_id)).start()

