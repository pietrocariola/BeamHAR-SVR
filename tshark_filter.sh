#!/bin/bash

# choose scenarios, persons, sessions to be processed
scenarios=("hall" "lab")
persons=("p01" "p02" "p03")
sessions=("s01")

for scenario in "${scenarios[@]}"; do
    for person in "${persons[@]}"; do
        for session in "${sessions[@]}"; do
            python pcap_splitter.py "$scenario" "$person" "$session"
        done
    done
done