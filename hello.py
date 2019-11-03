from flask import Flask, escape, request
import consul
import time
app = Flask(__name__)
c =consul.Consul()


@app.route('/')
def hello():
    return 'Hello, world'

@app.route('/lock/<name>')
def lock(name):
    index = None
    sessionID=c.session.create(name="Uli")
    #index, data = c.kv.get(name, index=index)
    worked= c.kv.put(name, 'uli', acquire=sessionID)
    print ("locking "+ str(worked))
    time.sleep(15)
    worked=c.kv.put(name, 'bar', release=sessionID)
    print ('Unlocking'+str(worked))
    return sessionID
