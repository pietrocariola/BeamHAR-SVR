#!/usr/bin/env bash

# add servers here
SERVERS=("192.168.1.4" "192.168.1.5")
BITRATES=("10M" "10M")
LENGTHS=("1400" "1400")
PROTOCOLS=("UDP" "TCP") 

# clean up group processes (and childs) when Ctrl+C
cleanup() {
    echo
    echo "Stopping all iperf3 processes..."
    kill 0
    exit 0
}

trap cleanup SIGINT

echo "Starting iperf3 tests in parallel"
echo "Press Ctrl+C to stop"
echo

for i in "${!SERVERS[@]}"; do

    SERVER="${SERVERS[$i]}"
    BITRATE="${BITRATES[$i]}"
    LENGTH="${LENGTHS[$i]}"
    PROTOCOL="${PROTOCOLS[$i]}"

    echo "Starting iperf3 for $SERVER"
    echo "Bitrate: "$BITRATE"bits/s"
    echo "Packet length: "$LENGTH"bytes"
    echo "Protocol: $PROTOCOL"
    echo

    while true; do
        if [ "$PROTOCOL" = "UDP" ]; then
            iperf3 -u -c "$SERVER" -b "$BITRATE" -l "$LENGTH"
        else
            iperf3 -c "$SERVER" -b "$BITRATE" -l "$LENGTH"        
        fi         
        sleep 1
    done &
done

wait
