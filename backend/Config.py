from flask import Flask
from elasticsearch import Elasticsearch, RequestsHttpConnection
from flask_socketio import SocketIO, emit
from flask_restful import Api

es = Elasticsearch(
    ['localhost:9200'],
    connection_class=RequestsHttpConnection
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['threaded'] = True
socketio = SocketIO(app, logger=True, engineio_logger=True)