#!/usr/bin/env python
###################################################################################
#                           Written by Wei, Hang                                  #
#                          weihanghank@gmail.com                                  #
###################################################################################
"""
Creates a pod using CoreV1Api from a yaml file.
"""
from __future__ import print_function
import time
from os import path
import yaml
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from pprint import pprint


def main():
    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.
    config.load_kube_config()

    with open(path.join(path.dirname(__file__), "apipod1.yaml")) as f:

        try:
            api_instance = client.CoreV1Api()
            namespace = 'default'
            body = yaml.safe_load(f)
            api_response = api_instance.create_namespaced_pod(namespace, body)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->create_namespaced_pod: %s\n" % e)


if __name__ == '__main__':
    main()
