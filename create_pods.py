#!/usr/bin/env python
###################################################################################
#                           Written by Wei, Hang                                  #
#                          weihanghank@gmail.com                                  #
###################################################################################
"""
Deploy pods to target system to test networkpolicies
This script does not create namespaces. Make sure all namespaces have been created.
"""
from __future__ import print_function
import time
from os import path
import yaml
import json
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from pprint import pprint
from my_py.k8s.data_input import read_data

DRY_RUN = False  # if it's False, means all policies will be delivered to cluster

DATA = read_data()  # input data from MMS or other policy orchestrator

# Following is the template to render REST API body of busy box pod
BASE_TEMPLATE = '''
apiVersion: v1
kind: Pod
metadata:
  labels:
    mms_network_tag: {mynet}
  name: {mynet}-pod
spec:
  containers:
  - image: yauritux/busybox-curl
    imagePullPolicy: IfNotPresent
    name: {mynet}-pod
    command: ["sh","-c","telnetd & sleep 10000"]
    resources: {{}}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
'''

POD_NO_LABELD = '''
apiVersion: v1
kind: Pod
metadata:
  name: {ns}-out
spec:
  containers:
  - image: yauritux/busybox-curl
    imagePullPolicy: IfNotPresent
    name: {ns}-out
    command: ["sh","-c","telnetd & sleep 10000"]
    resources: {{}}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
'''


def get_body():
    """
    Create a POD API body for each namespace, return a dictionary
    """
    _body = {}
    _nets = []
    for contract in DATA["contracts"]:
        _nets.extend(DATA["contracts"][contract]["provide_networks"] + DATA["contracts"][contract]["consume_networks"])

    nets = list(set(_nets))  # all nets but eliminate redundancy

    for net in nets:
        _body[net] = BASE_TEMPLATE.format(mynet=net)

    return _body


def main():
    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.

    bodies = get_body()
    for net in bodies:
        print(bodies[net])

    config.load_kube_config()

    try:
        api_instance = client.CoreV1Api()
        for namespace in DATA["namespaces"]:
            for net in bodies:
                body = yaml.load(bodies[net], Loader=yaml.FullLoader)
                if DRY_RUN:
                    api_response = api_instance.create_namespaced_pod(namespace, body, pretty="true",
                                                                      dry_run="All")
                else:
                    api_response = api_instance.create_namespaced_pod(namespace, body, pretty="true")
                    # pprint(api_response)  # used for diagnostics

            if not DRY_RUN: # create pod without label
                body_nolabel = yaml.load(POD_NO_LABELD.format(ns=namespace), Loader=yaml.FullLoader)
                api_response = api_instance.create_namespaced_pod(namespace, body_nolabel, pretty="true")

    except ApiException as e:
        print("Exception when calling APIs: %s\n" % e)


if __name__ == '__main__':
    main()
