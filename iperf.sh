#!/usr/bin/env bash

STAS=(
  "192.168.1.3"
)

RATE_PER_STA="10M"   # start low; increase later
PKT_LEN="1200"

for STA_IP in "${STAS[@]}"; do
  (
    while true; do
      iperf3 -c "$STA_IP" -u -b "$RATE_PER_STA" -l "$PKT_LEN" -t 60
      sleep 1
    done
  ) &
done

wait
