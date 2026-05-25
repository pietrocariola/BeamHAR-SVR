WIBFI = "./wibfi/main.py"

import subprocess
import os
import sys
import argparse
import csv

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

    wibfi = os.path.abspath(WIBFI)

    labels = os.path.abspath('./BeamHAR-SVR-Data/scenarios/'+scenario.lower()+'/'+person.upper()+'/'+session.upper()+'/annotations/activity_segments.csv')
    devices = os.path.abspath('./BeamHAR-SVR-Data/scenarios/'+scenario.lower()+'/'+person.upper()+'/'+session.upper()+'/annotations/devices.csv')
    pcap = os.path.abspath(devices+'/../../raw/capture.pcapng')
    outputs = os.path.abspath(devices+'/../../processed/')

    with open(labels, 'r') as file_labels:
        reader_labels = csv.DictReader(file_labels)
        # next(reader_labels)

        with open(devices, 'r') as file_devices:
            reader_devices = csv.DictReader(file_devices)
            # next(reader_devices)

            for i, label in enumerate(reader_labels):
                print(f"Label {i}")
                file_devices.seek(0)
                reader_devices = csv.DictReader(file_devices)
                for j, device in enumerate(reader_devices):
                    print(f"Device {j}")

                    cmd = [
                        'tshark',
                        '-r', pcap,
                        '-Y', 'frame.time >= "'+label['start_time']+'" && \
                                frame.time <= "'+label['end_time']+'" && \
                                wlan.vht.compressed_beamforming_report && \
                                wlan.addr=='+device['mac']
                    ]

                    result = subprocess.run(cmd, capture_output=True, text=True)
                    n_pkts = len(result.stdout.strip().split('\n'))
                    print(f"n_pkts: {n_pkts}")

                    file_name = f"{label['label'].lower()}_{device['device'].lower()}_{label['start_time'].replace(" ", "-")}"
                    file_name = os.path.abspath(os.path.join(outputs,file_name))
                    timestamp = f"{file_name}_timestamp" 
                    v = f"{file_name}_v" 
                    bfa = f"{file_name}_bfa"

                    print(device['standard'])
                    print(device['mimo'])
                    print(device['antennas'])
                    print(device['bandwidth'])
                    print(device['mac'])

                    cmd = [
                        sys.executable,
                        wibfi,
                        pcap,
                        device['standard'],
                        device['mimo'],
                        device['antennas'],
                        device['bandwidth'],
                        device['mac'],
                        str(n_pkts),
                        timestamp,
                        v,
                        bfa
                    ]
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    
