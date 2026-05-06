wpa_passphrase "NETGEAR93-5G" "shinycream130" > config
sudo wpa_supplicant -B -i wlp8s0 -c config
sudo dhclient wlp8s0
sudo airmon-ng start wlp8s0
sudo iw dev wlp8s0 set channel 44 80MHz
sudo tshark -i wlp8s0 -w capture.pcapng
