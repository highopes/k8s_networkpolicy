#!/usr/bin/env python
###################################################################################
#                           Written by Wei, Hang                                  #
#                          weihanghank@gmail.com                                  #
###################################################################################
"""
Creates networkpolicies using apiVersion: networking.k8s.io/v1 based on MMS Network Template Instance
"""
from __future__ import print_function
import time
from os import path
import yaml
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from pprint import pprint

# Following is the template to render REST API body
BASE_TEMPLATE = '''
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: 
  name: {mynet}
spec: 
  podSelector: 
    matchLabels: 
      mms_network_tag: {mynet}
  policyTypes: 
  - Ingress
  ingress: 
  - from: 
    - namespaceSelector: {{}}
      podSelector: 
        matchLabels:
          mms_network_tag: {mynet}
'''

FROM_TEMPLATE = '''
  - from: 
    - namespaceSelector: {{}}
      podSelector: 
        matchExpressions: 
          - {{key: mms_network_tag, operator: In, values: [{yournets}]}}
'''

PORTS_TEMPLATE = '''
    - protocol: {protocol}
      port: {port}
'''

# DATA should be the source data from MMS
'''
DATA = {
    "namespaces": ["test"],
    "contracts": {
        "usr2web": {
            "provide_networks": ["web"],
            "consume_networks": ["usr"],
            "ports": [
                {"protocol": "TCP", "port": "23"},
                {"protocol": "TCP", "port": "80"}
            ]
        },
        "web2db": {
            "provide_networks": ["db"],
            "consume_networks": ["web"],
            "ports": [
                {"protocol": "TCP", "port": "3306"},
                {"protocol": "TCP", "port": "23"}
            ]
        }
    }
}
'''
DATA = {
    "namespaces": ["test2"],
    "contracts": {
        "usr2web": {
            "provide_networks": ["web"],
            "consume_networks": ["usr"],
            "ports": [
                {"protocol": "TCP", "port": "23"},
                {"protocol": "TCP", "port": "80"}
            ]
        },
        "any2any": {
            "provide_networks": ["web", "vlan1", "vlan2", "vlan3"],
            "consume_networks": ["web", "vlan1", "vlan2", "vlan3"]
        }
    }
}


def get_body():
    """
    Create a Network Policy API body for each namespace, return a dictionary
    """
    _body = {}
    for contract in DATA["contracts"]:
        pnets = DATA["contracts"][contract]["provide_networks"]
        cnets = DATA["contracts"][contract]["consume_networks"]
        nets = list(set(pnets + cnets))  # all nets but eliminate redundancy
        for net in nets:
            if not _body.get(net):
                _body[net] = BASE_TEMPLATE.format(mynet=net)
            if net in pnets:
                if net in cnets:  # for those both in provide and consume
                    _body[net] += FROM_TEMPLATE.format(yournets=", ".join(nets))  # allow all other net in
                else:  # 'else' means 'provide only'
                    _body[net] += FROM_TEMPLATE.format(yournets=", ".join(cnets))  # only allow consume in
                if DATA["contracts"][contract].get("ports"):
                    _body[net] += "    ports: "
                    for port in DATA["contracts"][contract]["ports"]:
                        _body[net] += PORTS_TEMPLATE.format(protocol=port["protocol"], port=port["port"])
            else:  # for those consume net only
                _body[net] += FROM_TEMPLATE.format(yournets=", ".join(pnets))  # allow only provide net in

    return _body


def main():
    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.

    bodies = get_body()

    config.load_kube_config()

    try:
        api_instance = client.NetworkingV1Api()
        for namespace in DATA["namespaces"]:
            for net in bodies:
                body = yaml.load(bodies[net], Loader=yaml.FullLoader)
                api_response = api_instance.create_namespaced_network_policy(namespace, body, pretty="true",
                                                                             dry_run="All")
                # pprint(api_response)  # used for wet-run
                print(bodies[net])  # used for dry-run

    except ApiException as e:
        print("Exception when calling APIs: %s\n" % e)


if __name__ == '__main__':
    main()
