#!/bin/bash
env FLASK_APP=hello.py flask run --port 5001 &
env FLASK_APP=hello.py flask run --port 5002 &
env FLASK_APP=hello.py flask run --port 5003 &
