PCAP = "./test_captures/capture_andando.pcapng"
LABELS = ['sat', 'stand']
SUBJECTS = ['pietro', 'augusto']
START_TIMES = ["2026-04-27 16:15:49,106", "2026-04-27 16:15:59,000"]
END_TIMES = ["2026-04-27 16:15:59,000", "2026-04-27 16:19:00,000"]
SERVERS = [
#   [AC/AX, SU/MU, ATENNAS, BANDWIDTH, MAC]
    ['AC', 'SU', '4x1', '80', '02:c6:ff:32:c3:d1'],
    ['AC', 'SU', '4x1', '80', '02:c6:ff:32:c3:d1']
]
WI_BFI = "~/Wi-BFI/main.py"

import subprocess
# import pyshark
import os
# import sys
# import re

wi_bfi = os.path.expanduser(WI_BFI)

for i in range(len(LABELS)): 

    print(f"Label: {LABELS[i]}")

    for j, server in enumerate(SERVERS):

        print(f"Server: {server}")

        file_name = LABELS[i]+"_"+ \
        SUBJECTS[i]+"_"+ \
        START_TIMES[i].split(",")[0].replace("-", "").replace(" ","").replace(":", "") + \
        START_TIMES[i].split(",")[1][:3] + "_" + \
        END_TIMES[i].split(",")[0].replace("-", "").replace(" ","").replace(":", "") + \
        END_TIMES[i].split(",")[1][:3] + \
        server[4][:5].replace(":", "")

        new_pcap = file_name + ".pcapng"

        cmd = [
            'tshark',
            '-r', PCAP,
            '-Y', 'frame.time >= "'+START_TIMES[i]+'" && frame.time <= "'+END_TIMES[i]+'" && wlan.sa == '+server[4],
            '-w', './test_captures/'+new_pcap
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result)

        # pcap = pyshark.FileCapture(
        #     './test_captures/'+new_pcap,
        #     keep_packets=False,
        #     use_json=True
        # )   

        # print("counting pkts:")
        # n_packets = 0
        # for _ in pcap:
        #     print(f"'\r'{n_packets}", end="")
        #     n_packets += 1
        # print(f"\r{n_packets}", end="")
        # print("")

        # del(pcap)

        # result = subprocess.run(
        #     ["capinfos", f"./test_captures/{new_pcap}"],
        #     capture_output=True,
        #     text=True
        # )

        # match = re.search(r"Number of packets:\s+(\d+)", result.stdout)

        # if match:
        #     n_packets = int(match.group(1))
        #     print(n_packets)
        # else:
        #     print(f"Error: number of packets not found in capinfos")     

        # v = f"{file_name}_v" 
        # bfa = f"{file_name}_bfa"
        # print(f"V:{v}")
        # print(f"BFA:{bfa}")        

        # cmd = [
        #     sys.executable,
        #     wi_bfi,
        #     './test_captures/'+new_pcap,
        #     server[0],
        #     server[1],
        #     server[2],
        #     server[3],
        #     server[4],
        #     str(n_packets-18),
        #     v,
        #     bfa
        # ]
        # result = subprocess.run(cmd, capture_output=True, text=True)
        # print(result)