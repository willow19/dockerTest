from flask import Flask, send_from_directory
from redis import Redis, RedisError
import os
import socket
from apscheduler.schedulers.background import BackgroundScheduler

# Start the scheduler
sched = BackgroundScheduler()
sched.start()

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)

@app.route("/hello")
def hello():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Visits:</b> {visits}"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)

@app.route("/")
def index():
    return send_from_directory('.', 'index.html')

@app.route("/oauth")
def oauth():
    return send_from_directory('.', 'oauth.min.js')

def job_function():
    print "Hello World"

if __name__ == "__main__":  
    #sched.add_job(job_function, 'interval', seconds=20)
    app.run(host='0.0.0.0', port=80)
