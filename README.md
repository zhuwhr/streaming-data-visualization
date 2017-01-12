# Streaming-Data-Visualization
Streaming real time data using Accern API which consist of data captured from 20 million public websites or social medias. Basically, the unit is article. Similar articles can be grouped into stories which is about events happened on companies. The impact of the event is shown via an impact score representing the chance that an event may impact a company’s stock price by 1% at the end of trading day. 

First, we want to visualize the articles using dots with opacity 0.5. Now we look for highly dense area over the timeline which indicates there are a number of articles for that company in a short period of time. This might indicate some major episode of events happening at the company. Sentiment of article describes if the article was written positively or negatively by the author. It ranges from -1 to 1. So after indentifying an event we use a line chart to visualize the sentiment for that highly dense area of articles, to check if episode is having negative or positive sentiment.

### Video Link:https://vimeo.com/196806769
### Demo Link: http://nyuvis-web2.poly.edu/vis-fall2016/Streaming-Data-Monitoring-1
(note:-For now we are still not able to deploy our server on neigher Heroku or our university’s server. Once our mentor upload
our project on to the server, we can able to use the above link)

### Tools and components used (recommended) to setup the visualization
  1.  Python 
      Version: 2.7.12
      Download Link: https://www.python.org/downloads/release/python-2712/
  3.  Elasticsearch Database store
      Version: 5.0.2
      Download Link: https://www.elastic.co/downloads/elasticsearch
      Note: Elasticsearch will be installed locally and will use port 9200 i.e. (http://localhost:9200/)
      
### Steps for installing Python Packages and Modules
  1.  Install pip (Note: Python 2.7.9+ and 3.4+ comes with pip installed)
      - Install instruction: Download and run 'get-pip.py' (https://bootstrap.pypa.io/get-pip.py)
      - Reference: https://pip.pypa.io/en/stable/installing/#do-i-need-to-install-pip
  2.  Run command prompt/ terminal and execute following commands:
  
        1.  pip install flask
        2.  pip install flask_socketio
        3.  pip install flask_restful
        4.  pip install elasticsearch
        5.  pip install eventlet

### Steps for creating an index in elasticsearch
  1.  Start Python 2.7.12 console
  2.  Run the following commands:
  
      - from elasticsearch import Elasticsearch, RequestsHttpConnection
      - es = Elasticsearch(['localhost:9200'],connection_class=RequestsHttpConnection)
      - es.indices.create(index='articles')
     
### Steps for starting the Visualization
  1.  Clone this project 
  2.  Start Terminal/cmd and goto the project 'Streaming-Data-Monitoring-1 -> Backend' location by using cd command
  3.  Run command: "python app.py runserver 0.0.0.0:5000" (Note: This will run the Flask Server for the Visualization, it may take few seconds so wait untill its running then goto step 4)
      - 'app.py' is the server program to service requests from the frontend
  4.  Start another Terminal/cmd and goto the project 'Streaming-Data-Monitoring-1 -> Backend' location by using cd command
  5.  Run command: "python iviz.py"
      - 'iviz.py' is the script which downloads real time data using the ACCERN API and sends to app.py server to save it in elasticsearch and also broadcast it to all frontend running using websockets
  6.  Start web browser and start link: http://127.0.0.1:5000/ or http://yourIPaddress:5000/
(Note: Since the backend will start getting the data using ACCERN API, it will take some time to fill the main view depending on how fast ACCERN API provides the article data)
      

 
