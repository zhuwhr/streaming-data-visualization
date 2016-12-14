import eventlet
eventlet.monkey_patch()


from Backend.Mediator import *
from Backend.Config import *


@app.route('/')
def index():
    return render_template('index1.html', async_mode=socketio.async_mode)

@socketio.on('get_all_articles', namespace='/articles')
def articles(message):
    re = es.search(index='articles', doc_type='article', body={"query": {"match_all": {}}},size=10000)
    responseData = re['hits']
    emit('my_response',
         {'data': json.dumps(responseData['hits'], sort_keys=False, indent=2)},broadcast=True)

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
    socketio.run(app, debug=True)

