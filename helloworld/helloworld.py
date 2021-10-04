from flask import Flask, abort

from kubernetes import client, config
from kubernetes.client import configuration

import requests, os
import pymongo

app = Flask(__name__)

@app.route("/")
def hello_world():
    return 'Hello, World!'

@app.route("/health")
def health():
    try:
        myclient = pymongo.MongoClient("mongodb://database:27017/")
        myclient.close()

        return "OK"
    except:
        abort(500)

@app.route("/diag")
def diag():
    config.load_incluster_config()

    k8s_client = client.CoreV1Api()

    print("\nList of pods")
    pod_data = {}
    for i in k8s_client.list_pod_for_all_namespaces().items:
        try:
            print("%s\t%s\t%s" %
                (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
            if i.metadata.namespace == "default":
                pod_data[i.metadata.name] = {}
                pod_data[i.metadata.name]["pod_ip"]  = i.status.pod_ip
                pod_data[i.metadata.name]["host_ip"]  = i.status.host_ip
        
                resp = requests.get(f"http://{i.status.pod_ip}/health", timeout=0.001)
                pod_data[i.metadata.name]["health"] = resp.text

                print(i.spec.containers)
                for container in i.spec.containers:
                    if "nginx" in container.image:
                        try:
                            pod_data[i.metadata.name]["nginx_version"] = container.image.split(':')[-1]
                        except:
                            pod_data[i.metadata.name]["nginx_version"] = "UnableToRetrieve"
        except Exception as e:
            print(str(e))
            if i.metadata.name in pod_data:
                pod_data[i.metadata.name]["diag_error"] = True

    node_data = {}
    for i in k8s_client.list_node().items:
        try:
            print(f"{i.metadata.name}\t{i.status.addresses}")
            node_data[i.metadata.name] = {}
            node_data[i.metadata.name]["addresses"] = [x.address for x in i.status.addresses]
        except Exception as e:
            print(str(e))
            if i.metadata.name in node_data:
                node_data[i.metadata.name]["diag_error"] = True

    
    return {"pod_data": pod_data, "node_data": node_data}

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', threaded=True, debug=True, port=80)
