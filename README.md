This project you are assumes that you are using a system with 2 or more network interfaces in bridged mode. The original design was based on an OrangePi R1 http://www.orangepi.org/OrangePiR1/


# Setup Instructions

## c2 Server Setup Instructions
 - pip install -r requirements.txt
 - python Server.py

## MITM Node Setup Instructions
 - apt install bridge-utils build-essential python-dev libnetfilter-queue-dev
 - pip install NetfilterQueue websocket-client
 - pip install git+https://github.com/dpallot/simple-websocket-server.git
 - Setup bridge networking https://wiki.debian.org/BridgeNetworkConnections

```
auto br0
iface br0 inet dhcp
        bridge_ports eth0 eth1
        bridge_stp off
        bridge_fd 0
        bridge_maxwait 0
```

 - sudo python Bot.py

 
