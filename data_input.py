#!/usr/bin/env python
###################################################################################
#                           Written by Wei, Hang                                  #
#                          weihanghank@gmail.com                                  #
###################################################################################
"""
Extract raw data from json file, and return python element after processing (incl. name conversion)
"""
from __future__ import print_function
from os import path
import json


def read_data():
    # extract policy from json file. In a complete system, should be replaced by MMS or other orchestrator data source
    try:
        with open(path.join(path.dirname(__file__), "input_data.json")) as f:
            data = json.load(f)

    except FileNotFoundError as e:
        print("Input Data File Not Found!")
        exit(1)

    # convert network name from MMS' underline style
    for c in data["contracts"]:
        data["contracts"][c]["provide_networks"] = [n.replace("_", "-") for n in
                                                    data["contracts"][c]["provide_networks"]]
        data["contracts"][c]["consume_networks"] = [n.replace("_", "-") for n in
                                                    data["contracts"][c]["consume_networks"]]
    if data.get("expose"):
        for ex in data["expose"]:
            n = ex["network"]
            ex["network"] = n.replace("_", "-")

    return data
