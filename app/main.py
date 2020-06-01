import os
import unicodedata
import hvac
from flask import Flask
from cassandra.cluster import  Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import tuple_factory


app = Flask(__name__)

@app.route("/getstring")
def get():
    return "Hello AWS"

@app.route("/getdata")    
def get_data():
    f = open('/var/run/secrets/kubernetes.io/serviceaccount/token')
    jwt = f.read()
    client = hvac.Client()
    client = hvac.Client(url='http://ec2-54-172-90-34.compute-1.amazonaws.com:8200')
    client.auth_kubernetes("webapp", jwt)
    #client.auth_kubernetes("webapp", "eyJhbGciOiJSUzI1NiIsImtpZCI6InM0LW9veUpxalY4LVI4VUNRSlFCMnlRUnV6VENlMW83U0ZmZ2hiTVplWmcifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi1hY2NvdW50LXRva2VuLWJudHJ3Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLWFjY291bnQiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiI0ZGYwN2MzNC1kOTc0LTQzODQtOGJjMC01NGM5ZGIzYjJlZWIiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06YWRtaW4tYWNjb3VudCJ9.XEIlqZ8bJ1qCMuMhuvc2zk1Yr1my6uUiP2lBVrTacPMIMz2Nc4_Mu4d6X4OavMVy2LMcAjATbbRI3MKias6DGOTtF6eGvlTjWytu-4Td3UXkYwAhANtqOC5RosWIZXMXmrDjROT2c0-Io1F0XV88sdoQTIA8j1fWrA1HdhIHuTMPk-C9c0gi9N0dSxP0ar16npei7oZtfrgIRlcC4eFJ2PnL00A4yKaolDgVDCVjfp3IEBBMa9ZaqoNh1YlN0OWSciO-0E31JMcE7GbEk9snqut2Bt36aQSYVFsVlKsVUR7NwJBKC-1Pf9_mOn-m_ugg6U3AC3rfYJ3X1dhBGEDKBA")
    read_response = client.read("database/creds/my-role")
    username = read_response.get("data").get("username")
    password = read_response.get("data").get("password")
    print("username :"+ username)
    print("password :"+ password)
    auth_provider = PlainTextAuthProvider(username=username, password=password)
    cluster = Cluster(contact_points=["100.25.10.11"],auth_provider=auth_provider, protocol_version=4)    
    session = cluster.connect('test_keyspace')   
    session.row_factory = tuple_factory 
    result = session.execute("select * from test_keyspace.employee")  
    return str.join(u'\n',map(str,result))

if __name__ == "__main__":
    app.run(host='0.0.0.0')
