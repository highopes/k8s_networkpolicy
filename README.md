# Using ACI or MMS Group-based Policies for Kubernetes Environment

## Description

Neither the network nor the application people are familiar with the way network policies are defined in Kubernetes. This project implements the popular group-based network policy model in a CNI environment that supports k8s's network policy API. For automation systems using Group-based Policy (e.g., Multi-cloud-network Middleware Systems, MMS), by defining a unified template that can be defined once and reused multiple times, you can automate and unify multi-cloud policy deployment without having to learn multi-cloud network configuration one by one.

## Functions

* The basic logic of Group-based Policy is to connect the cloud workload to the network providing the service (provider network) and the network using the service (consumer network) independent of addresses, infrastructure elements (e.g. VLANs, etc.). Communication can only occur between networks that have directly established a relationship for service provisioning or consuming, and the policies to establish such mutual relationship is called a contract.

* The service providers are generally considered to have a higher security level, and they have no restrictions on access to the consumers, while visitors can only use the protocols and ports specified by the providers.

* For a contract, a network can be both a provider and a consumer, thus establishing mutual communication with other parties while keeping itself secure.

* Both the service provider network and the service consumer network are protected externally, i.e. other pods cannot access them directly, but only through the published services, and these accesses will belong to the north-south traffic subject to other security mechanisms.

## Limitations

Due to the limitations of the Kubernetes Network Policy feature, the Group Policy capabilities that can be implemented are not exactly equivalent to Group Policy features such as ACI EPG.

* Only 'permit' statement is currently supported (whitelist mechanism)

* The source port number in the contract is ignored

* The 'established' setting in the contract is ignored

## Environment

* Python 3+

* Kubernetes Client Library for python

## Usage

* aci2k8s.py: Push the Group-based Policies to Kubernetes cluster (make sure the kubeconfig is in ~/.kube directory with the proper authorization). Different network policies can be implemented by modifying the DATA variable.

* create_pods.py: Any Kubernetes resource with the label mms_network_tag=<network name> can join the network specified by the name. This script automatically creates a number of test pods that are tagged to join all the networks involved in the network policy, and automatically generates a pod without a tag for comparison in the test. Make sure to use the same DATA data as the previous scripts.

* clear_pods_np.py: Clear the network policies and test pods generated by the first two scripts. Make sure to use the same DATA data as the first two scripts.
