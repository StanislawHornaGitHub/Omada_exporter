switch_value_map: dict[str, dict] = {
    "linkStatus": {
        0: "Down",
        1: "Up"
    },
    "linkSpeed": {
        -1: "Down",
        0: "Auto",
        1: "10M",
        2: "100M",
        3: "1000M",
        4: "2500M",
        5: "10G",
        6: "5G",
    },
    "duplex": {
        -1: "Down",
        0: "Auto",
        1: "Half",
        2: "Full",
    },
    "mirrorMode": {
        0: "ingress",
        1: "egress",
        2: "ingress and egress",
    },
}

router_value_map: dict[str, dict] = {
    "status": switch_value_map["linkStatus"],
    "speed": switch_value_map["linkSpeed"],
    "duplex": switch_value_map["duplex"],
    "onlineDetection": {
        -1: "N/A",
        0: "No",
        1: "Yes",
    },
    "mode": {
        -1: "N/A",
        0: "WAN",
        1: "LAN",
    },
    "internetState": {
        0: "Offline",
        1: "Online",
    },
}

access_point_value_map: dict[str, dict] = {
    "rate": {
        "0": "Down",
        "10": "10M",
        "100": "100M",
        "1000": "1000M",
        "2500": "2500M",
        "10000": "10G",
    },
    "duplex": switch_value_map["duplex"]
}