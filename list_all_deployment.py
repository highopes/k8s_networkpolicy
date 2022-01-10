#!/usr/bin/env python
###################################################################################
#                           Written by Wei, Hang                                  #
#                          weihanghank@gmail.com                                  #
###################################################################################
"""
List all deployments using AppsV1Api
"""

from kubernetes import client, config
from kubernetes.client.rest import ApiException
from pprint import pprint


def main():
    # Configs can be set in Configuration class directly or using helper utility
    config.load_kube_config()

    try:
        v1 = client.AppsV1Api()
        ret = v1.list_deployment_for_all_namespaces(watch=False, pretty='true')
        pprint(ret)
    except ApiException as e:
        print("Exception when calling AppsV1Api->list_deployment_for_all_namespaces: %s\n" % e)


if __name__ == '__main__':
    main()
