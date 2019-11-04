from flask import Flask, request, render_template
import consul
import json


app = Flask(__name__)
c = consul.Consul()


def convert_to_dict(obj):
    obj_dict = {
        "__class__": obj.__class__.__name__,
        "__module__": obj.__module__
    }
    obj_dict.update(obj.__dict__)
    return obj_dict


class MyData:
    def __init__(self):
        sessionID=""
        locked=""
        lockField=""
        error=""


class LockStatus:
    def __init__(self):
        isLocked=False
        keyExists=False
        lockholderSession=""


MASTERLOCK = "MASTERLOCK"
LOCKSPATH = "locks"


def getMasterLock():
    return getLockRaw(MASTERLOCK, "Masterlock")


def releaseMasterLock(session):    
    return releaseLockRaw(MASTERLOCK, session)


def getLock(name):
    return getLockRaw(LOCKSPATH+"/" + name, name)


def getLockRaw(path, name):
    session = c.session.create(name=name)
    worked = c.kv.put(path, name, acquire=session)    
    return worked, session


def releaseLock(name, session):
    return releaseLockRaw(LOCKSPATH+"/" + name, session)


def releaseLockRaw(path, session):
    worked = c.kv.put(path, path, release=session)
    c.session.destroy(session, dc=None)
    return worked


def isLocked(name):
    isLocked = False
    keyExists = False
    session = ""
    try:
        index, values = c.kv.get(LOCKSPATH+"/" + name)
        print("Session:" + index + " " + str(values))
        if values is not None:
            print("Vals")
            keyExists = True
    except TypeError:
        print("TypeError:" + session)
        keyExists = False
    try:
        if keyExists:
            index, values = c.kv.get(LOCKSPATH+"/" + name)    
            session = values['Session']
            print("Session:" + session)
            isLocked = True
    except (KeyError, TypeError):
        print("XXX:")
        isLocked = False
    return isLocked, keyExists, session


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/')
def hello():
    mData = MyData()
    mData.lockField = "Uli"
    return render_template('index.html', mData=mData)


@app.route('/exit')
def exit():
    shutdown_server()
    return 'Server shutting down...'


@app.route('/isLocked/<name>')
def isLockSet(name):
    lock = LockStatus()
    lock.isLocked, lock.keyExists, lock.session = isLocked(name)
    return json.dumps(lock, default=convert_to_dict, indent=4, sort_keys=True)


@app.route('/lock/<name>')
def lock(name):
    mData = MyData()
    mData.lockField = name
    mData.error = ""
    masterLockAquired, masterLockSession = getMasterLock()
    if masterLockAquired:
        worked, mData.sessionID = getLock(name)
        if worked:
            mData.locked = "Locked"
        else:
            mData.locked = "Failed"
            lock = LockStatus()
            lock.isLocked, lock.keyExists, lock.session = isLocked(name)
            mData.error += " already locked: " + str(lock.isLocked)
            mData.error += " key exists: " + str(lock.isLocked)
            mData.error += " holder session: " + str(lock.session)
        masterLockReleased = releaseMasterLock(masterLockSession)
    else:
        mData.locked = "NOMASTERLOCK"
    return json.dumps(mData, default=convert_to_dict, indent=4, sort_keys=True)


@app.route('/lockMultiple/<names>') 
def lockMultiple(names):
    mData = MyData()
    mData.lockField = names
    nameList = names.split(";")
    mData.error = ""

    masterLockAquired, masterLockSession = getMasterLock()
    if masterLockAquired:
        isAnyItemInListLocked = False
        for name in nameList:
            isKeyLocked, keyExists, session = isLocked(name)
            mData.error += " Field: " + name
            mData.error += " already locked: " + str(isKeyLocked)
            mData.error += " key exists: " + str(keyExists)
            mData.error += " holder session: " + str(session)
            if isKeyLocked:
                isAnyItemInListLocked = True
            else:
                print(name+" free")
        if not isAnyItemInListLocked:
            for name in nameList:
                print(name+" tryingLock ")
                worked, mData.sessionID = getLock(name)     
                print(name+" tryingLock " + str(worked) + " " + str(mData.sessionID))
                if worked:
                    mData.locked = "all Locked"
                else:
                    mData.locked = "REFUSED"
        else:
            mData.locked = "REFUSED"        
        masterLockReleased = releaseMasterLock(masterLockSession)
    else:
        mData.locked = "NOMASTERLOCK"
    return json.dumps(mData, default=convert_to_dict, indent=4, sort_keys=True)


@app.route('/unlock/<name>', methods=['POST', 'GET'])
def unlock(name):
    
    mData = MyData()
    mData.lockField = name
    mData.sessionID = request.args.get('SessionID')

    masterLockAquired, masterLockSession = getMasterLock()
    if masterLockAquired:
    
        worked = releaseLock(name, mData.sessionID)
        if worked:
            mData.locked = "UnLocked"
        else:
            mData.locked = "Could Not Unlock"        
        masterLockReleased = releaseMasterLock(masterLockSession)
    else:
        mData.locked = "NOMASTERLOCK"

    return json.dumps(mData, default=convert_to_dict, indent=4, sort_keys=True)


@app.route('/unlockMultiple/<names>') 
def unlockMultiple(names):
    mData = MyData()
    mData.lockField = names
    mData.error = ""
    mData.sessionID = request.args.get('SessionID')
    nameList = names.split(";")

    masterLockAquired, masterLockSession = getMasterLock()
    if masterLockAquired:
        for name in nameList:
            releaseLock(name, mData.sessionID)
            mData.error += "Name:" + name + "released"
        mData.locked = "are UnLocked"
        masterLockReleased = releaseMasterLock(masterLockSession)
    else:
        mData.locked = "NOMASTERLOCK"
    return json.dumps(mData, default=convert_to_dict, indent=4, sort_keys=True)


