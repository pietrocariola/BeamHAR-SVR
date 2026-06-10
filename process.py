WIBFI = "./wibfi/main.py"

import subprocess
import os
import sys
import argparse
import csv

def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print(f"WARNING: {file_path.split("/")[-1]} does not exist")

if __name__=='__main__':

    # Create a command-line argument parser
    parser = argparse.ArgumentParser()

    # Define command-line arguments
    parser.add_argument('scenario', help='hall, lab, ...')
    parser.add_argument('person', help='P01, P02, P03, ...')
    parser.add_argument('session', help='S01, S02, S03, ...')    

    # Parse the command-line arguments
    args = parser.parse_args()

    # Set variables based on command-line arguments
    scenario = args.scenario.lower()
    person = args.person.lower()
    session = args.session.lower()

    print(f"{scenario} | {person} | {session}")

    wibfi = os.path.abspath(WIBFI)

    labels = os.path.abspath('./BeamHAR-SVR-Data/scenarios/'+scenario+'/'+person+ \
                             '/'+session+'/annotations/activity_segments.csv')
    devices = os.path.abspath('./BeamHAR-SVR-Data/scenarios/'+scenario+'/'+person+ \
                              '/'+session+'/annotations/devices.csv')
    captures = os.path.abspath('./BeamHAR-SVR-Data/scenarios/'+scenario+'/'+person+ \
                              '/'+session+'/raw/')
    outputs = os.path.abspath('./BeamHAR-SVR-Data/scenarios/'+scenario+'/'+person+ \
                              '/'+session+'/processed/')

    pcap = os.path.join(captures, 'capture.pcapng')
    pcap_mimo = os.path.join(captures, 'capture_mimo.pcapng')

    print(f"Filtering mimo control packets...")
    cmd = [
        'tshark',
        '-r', pcap,
        '-Y', 'wlan.vht.mimo_control.feedbacktype && wlan.vht.mimo_control.feedbacktype == MU',
        '-w', pcap_mimo
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    with open(labels, 'r') as file_labels:
        reader_labels = csv.DictReader(file_labels)

        with open(devices, 'r') as file_devices:
            reader_devices = csv.DictReader(file_devices)

            for device in reader_devices:
                pcap_device = os.path.join(captures, 'capture_device.pcapng')
                print(f"Filtering device {device['device'].lower()}...")
                cmd = [
                    'tshark',
                    '-r', pcap_mimo,
                    '-Y', f"wlan.addr=={device['mac']}",
                    '-w', pcap_device
                ]
                result = subprocess.run(cmd, capture_output=True, text=True)
                file_labels.seek(0)
                reader_labels = csv.DictReader(file_labels)
                for label in reader_labels:
                    label['label'] = label['label'].replace("/", " ")
                    pcap_timestamp = os.path.join(captures, 'capture_timestamp.pcapng')
                    sys.stdout.write("\033[2K\r")
                    print(f"Label ({label['label'].lower()},{label['person'].lower()})...", end="\r")
                    cmd = [
                        'tshark',
                        '-r', pcap_device,
                        '-Y', 'frame.time >= "%s" && frame.time <= "%s"' % (label['start_time'], label['end_time']),
                        '-w', pcap_timestamp
                    ]
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    file_name = f"{label['label'].lower()}_{label['person'].lower()}_{ \
                        device['device'].lower()}_{label['start_time'].replace(" ", "-").replace(":", "-")}"
                    file_name = os.path.abspath(os.path.join(outputs, file_name))
                    timestamp = f"{file_name}_timestamp" 
                    v = f"{file_name}_v" 
                    bfa = f"{file_name}_bfa"
                    cmd = [
                        sys.executable,
                        wibfi,
                        pcap_timestamp,
                        device['standard'],
                        device['antennas'],
                        device['bandwidth'],
                        device['mac'],
                        timestamp,
                        v,
                        bfa
                    ]
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    remove_file(pcap_timestamp)
                remove_file(pcap_device)
    remove_file(pcap_mimo)