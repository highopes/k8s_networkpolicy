#!/usr/bin/env python
###################################################################################
#                           Written by Wei, Hang                                  #
#                          weihanghank@gmail.com                                  #
###################################################################################
"""
Deploy pods to target system to test networkpolicies
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

Clear_Pods = True
Clear_NetworkPolicies = True

DATA = read_data()  # input data from MMS or other policy orchestrator


def get_nets():
    """
    get and return all networks
    """
    _nets = []
    for contract in DATA["contracts"]:
        _nets.extend(DATA["contracts"][contract]["provide_networks"] + DATA["contracts"][contract]["consume_networks"])

    nets = list(set(_nets))  # all nets but eliminate redundancy

    return nets


def main():
    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.

    all_net = get_nets()

    config.load_kube_config()

    try:
        core_inst = client.CoreV1Api()
        net_inst = client.NetworkingV1Api()
        for ns in DATA["namespaces"]:
            for net in all_net:
                if Clear_Pods:
                    core_inst.delete_namespaced_pod(name=net + "-pod", namespace=ns, grace_period_seconds=0)
                if Clear_NetworkPolicies:
                    net_inst.delete_namespaced_network_policy(name=net, namespace=ns, grace_period_seconds=0)
            if Clear_Pods:
                core_inst.delete_namespaced_pod(name=ns + "-out", namespace=ns, grace_period_seconds=0)

    except ApiException as e:
        print("Exception when calling APIs: %s\n" % e)


if __name__ == '__main__':
    main()
