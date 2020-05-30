import os
import hvac
from flask import Flask
app = Flask(__name__)

@app.route("/get")
def get():
    return "Hello AWS"

@app.route("/")
def hello():    
    f = open('/var/run/secrets/kubernetes.io/serviceaccount/token')
    jwt = f.read()
    client = hvac.Client()
    client = hvac.Client(url='http://ec2-54-209-168-51.compute-1.amazonaws.com:8200')
    client.auth_kubernetes("webapp", jwt)
    read_response = client.secrets.kv.read_secret_version(path='ashok')
    return read_response['data']['data']

if __name__ == "__main__":
    app.run(host='0.0.0.0')
