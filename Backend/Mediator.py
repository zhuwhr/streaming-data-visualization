from flask import jsonify, url_for, redirect, request
from flask_restful import Resource
from flask import render_template,request
import json
#Custome Imports
from Backend.Config import *


class Mediator(Resource):

    def get(self,keyword=None):
        return

    def post(self):
        print(request)
        data = request.get_json()
        print('Article indexed into elasticsearch...')
        print(data)
        es.index(index='articles', doc_type='article', body=data)
        source = {}
        newData = {'list': []}
        source['_source']= data
        newData['list'].append(source)
        socketio.emit('my_response', {'data': newData['list']}, namespace='/articles')






