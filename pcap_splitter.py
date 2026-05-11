PCAP = "./test_captures/capture_andando.pcapng"
LABELS = ['sat', 'stand']
SUBJECTS = ['pietro', 'augusto']
START_TIMES = ["2026-04-27 16:15:49,106", "2026-04-27 16:15:49,113070362"]
END_TIMES = ["2026-04-27 16:15:59,000", "2026-04-27 16:15:59,000"]
SERVERS = [
#   [AC/AX, SU/MU, ATENNAS, BANDWIDTH, MAC]
    ['AC', 'SU', '4x1', '80', '02:c6:ff:32:c3:d1'],
    ['AC', 'SU', '4x1', '80', '02:c6:ff:32:c3:d1']
]
WI_BFI = "~/Wi-BFI/main.py"

MAX_PCAP_SIZE = 1e100

import subprocess
import pyshark
import os
import sys

wi_bfi = os.path.expanduser(WI_BFI)

for i in range(len(LABELS)): 

    file_name = LABELS[i]+"_"+ \
    SUBJECTS[i]+"_"+ \
    START_TIMES[i].split(",")[0].replace("-", "").replace(" ","").replace(":", "") + \
    START_TIMES[i].split(",")[1][:3] + "_" + \
    END_TIMES[i].split(",")[0].replace("-", "").replace(" ","").replace(":", "") + \
    END_TIMES[i].split(",")[1][:3] \

    new_pcap = file_name + ".pcapng"
    print(f"new pcap file: {new_pcap}")

    cmd = [
        'tshark',
        '-r', PCAP,
        '-Y', 'frame.time >= "'+START_TIMES[i]+'" && frame.time <= "'+END_TIMES[i]+'"',
        '-w', './test_captures/'+new_pcap
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result)

    pcap = pyshark.FileCapture(
        PCAP,
        keep_packets=False,
        use_json=True
    )   

    # print("counting pkts:")
    # pkts = 0
    # for _ in pcap:
    #     print(f"'\r'{pkts}", end="")
    #     pkts += 1
    # print(f"\r{pkts}", end="")
    # print("")

    print("deleting file capture")
    del(pcap)
    print("file capture deleted")

    print("looping through servers")
    for j, server in enumerate(SERVERS):

        print(f"running for server {j}")

        v = f"{file_name}_{server[4]}_v".replace(":", "") 
        bfa = f"{file_name}_{server[4]}_bfa".replace(":", "")
        print(f"V:{v}")
        print(f"BFA:{bfa}")

        

        cmd = [
            sys.executable,
            wi_bfi,
            './test_captures/'+new_pcap,
            server[0],
            server[1],
            server[2],
            server[3],
            server[4], "2",
            # str(MAX_PCAP_SIZE),
            v,
            bfa
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result)