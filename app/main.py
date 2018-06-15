from flask import Flask, request, abort, redirect, url_for, jsonify, render_template
import json
import redis
import datetime, time
import ast
from rejson import Client, Path

REDIS_SERVER = 'redis-master'
REDIS_PWD = ''
TTL = 31104000

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Read Usage API Docs'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/webhook', methods=['POST'])
def webhook_save():
    if request.method == 'POST':
        timestamp_human = datetime.datetime.now()
        timestamp = int(time.time())
        nowDatetime = timestamp_human.strftime('%Y-%m-%d(%H:%M:%S)')
        req_data = request.get_json()
        alertname = req_data['commonLabels']['alertname']
        severity = ''
        receiver = req_data['receiver']
        key_name = str(timestamp)+"_"+alertname+"_"+receiver    
        try:
            #conn = redis.Redis(host=REDIS_SERVER, port=6379, db=0, password=REDIS_PWD)
            conn = Client(host=REDIS_SERVER, port=6379, db=0, password=REDIS_PWD)
            conn.ping()
            print 'Redis connected %s' % (REDIS_SERVER)
        except Exception as e:
            print 'Error:', e
            exit('Failed to connecting')   

        conn = Client(host=REDIS_SERVER, port=6379)
        conn.jsonset(key_name, Path.rootPath(), req_data)
        data = json.dumps(conn.jsonget(key_name))
        print data
        # Redis : SCAN 0 match 1527911[1-9][1-9]*
        
    else:
        abort(400)

    if not conn.exists(key_name):
        print "Error: %s is doesn't exist" % (key_name)
    

    return jsonify({'status':'success'}), 200

@app.route('/api/v1/view/')
def page_not_found():
    return redirect(url_for('hello'))
@app.route('/api/v1/view/<timestamp>/<alert_type>/<reciever>')
def webhook_view(timestamp=None, alert_type=None, reciever=None, key_name=None):
    if request.method == 'GET':
        conn = Client(host=REDIS_SERVER, port=6379, db=0, password=REDIS_PWD)
        params = timestamp+'_'+alert_type+'_'+reciever
        data = json.dumps(conn.jsonget(params))
        return render_template('info.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
