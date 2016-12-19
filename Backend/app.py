import eventlet
eventlet.monkey_patch()

from dateutil import parser
from datetime import datetime
from dateutil import tz

from Backend.Mediator import *
from Backend.Config import *


@app.route('/')
def index():
    return render_template('index1.html', async_mode=socketio.async_mode)

@socketio.on('get_all_articles', namespace='/articles')
def articles(message):
    re = es.search(index='articles', doc_type='article', body={"query": {"match_all": {}}},size=10000)
    responseData = re['hits']['hits']
    for artcle in responseData:
        emit('my_response',
             {'data': json.dumps(artcle, sort_keys=False, indent=2)})

@socketio.on('get_sector_articles', namespace='/articles')
def get_sector_articles(message):
    sector = message['data']
    re = es.search(index='articles', doc_type='article',body={"query": {"bool": {"must":[{"match":{"entities.sector":sector}}]}}},size=10000)
    responseData = re['hits']['hits']
    companySet = {"company":7}
    companySet.clear()
    dicto = {"hits":[]}
    data_to_send = {"hits":[]}
    today = datetime.utcnow().date()
    current = datetime(today.year, today.month, today.day, tzinfo=tz.tzutc())
    for artcle in responseData:
        if artcle['_source']['entities'][0]['sector'] != sector:
            continue
        articleDate = parser.parse(artcle['_source']['harvested_at'])
        compareDate = datetime(articleDate.year, articleDate.month, articleDate.day, tzinfo=tz.tzutc())
        if compareDate == current:
            if artcle['_source']['entities'][0]['ticker'] not in companySet:
                companySet[artcle['_source']['entities'][0]['ticker']] = 0
            else:
                tempCt = companySet[artcle['_source']['entities'][0]['ticker']] + 1
                companySet[artcle['_source']['entities'][0]['ticker']] = tempCt
            dicto['hits'].append(artcle)
    sortedCompanies = sorted(companySet, key=companySet.get, reverse=True)[:10]

    for artcle in dicto['hits']:
        if artcle['_source']['entities'][0]['ticker'] in sortedCompanies:
            data_to_send['hits'].append(artcle)

    emit('receiveSectorArticle',{'data': data_to_send['hits']})

@socketio.on('get_allSector_articles', namespace='/articles')
def get_allSector_articles(message):
    re = es.search(index='articles', doc_type='article', body={"query": {"match_all": {}}}, size=10000)
    responseData = re['hits']['hits']
    dicto = {"hits": []}
    today = datetime.utcnow().date()
    current = datetime(today.year, today.month, today.day, tzinfo=tz.tzutc())
    for artcle in responseData:
        articleDate = parser.parse(artcle['_source']['harvested_at'])
        compareDate = datetime(articleDate.year, articleDate.month, articleDate.day, tzinfo=tz.tzutc())
        if compareDate == current:
            dicto['hits'].append(artcle)
    emit('receiveAllSectorArticle', {'data': dicto['hits']}, broadcast=True)

@socketio.on('get_allSectors', namespace='/articles')
def get_allSectors(message):
    re = es.search(index='articles', doc_type='article', body={"query": {"match_all": {}}}, size=10000)
    responseData = re['hits']['hits']
    dicto = {}
    for artcle in responseData:
        if (artcle['_source']['entities'][0]['sector'] not in dicto):
            dicto[artcle['_source']['entities'][0]['sector']] = 1
        else:
            artcle_ct = dicto[artcle['_source']['entities'][0]['sector']] + 1
            dicto[artcle['_source']['entities'][0]['sector']] = artcle_ct
    sortedCompanies = sorted(dicto, key=dicto.get, reverse=True)
    sortedCompanies.remove('N/A')
    sortedCompanies.remove('n/a')

    emit('receiveAllSectors', {'data': sortedCompanies})

@socketio.on('get_top_articles', namespace='/articles')
def get_top_articles(message):
    re = es.search(index='articles', doc_type='article',body={"query": {"match_all": {}}},size=10000)
    responseData = re['hits']['hits']
    companies = set()
    dicto = {'Age': 7}
    dicto.clear()
    for artcle in responseData:
        if artcle['_source']['entities'][0]['ticker'] not in companies:
            companies.add(artcle['_source']['entities'][0]['ticker'])
    for company in companies:
        temparticle = es.search(index='articles', doc_type='article',body={"query": {"bool": {"must":[{"match":{"entities.ticker":company}}]}}},size=10000)
        count = temparticle['hits']['total']
        dicto[company] = count

    newA = sorted(dicto, key=dicto.get, reverse=True)[:5]

    for tickerVal in newA:
        re = es.search(index='articles', doc_type='article',body={"query": {"bool": {"must":[{"match":{"entities.ticker":tickerVal}}]}}},size=10000)
        emit('my_response',
             {'data': re['hits']['hits']}, broadcast=True)

@socketio.on('get_articles', namespace='/articles')
def get_company_articles(message):
    company = message['data']
    re = es.search(index='articles', doc_type='article',body={"query": {"bool": {"must":[{"match":{"entities.ticker":company}}]}}},size=10000)
    responseData = re['hits']['hits']
    emit('my_response',
          {'data': json.dumps(responseData, sort_keys = False, indent = 2)},broadcast=True)

api = Api(app)
api.add_resource(Mediator, "/api/article", endpoint="article")

if __name__ == '__main__':
    #socketio.run(app,host= '0.0.0.0', port=5000, debug=False)
    socketio.run(app, debug=False)

