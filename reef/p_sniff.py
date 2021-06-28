import scapy.all as scapy
from scapy.layers.http import HTTPRequest
from scapy.layers.inet import IP
from scapy.packet import Raw

class Sniffer:
    def __init__(self, iface):
        self.iface = iface

    def sniff_packets(self):
        if self.iface:
            scapy.sniff( prn=self.process, store=True, iface=self.iface)
        else:
            print('No interface selected so using default')
            scapy.sniff(prn=self.process, store=True)

    def process(self, pkt: scapy.Packet):
        if pkt.haslayer(HTTPRequest):
            url = pkt[HTTPRequest].Host.decode()+pkt[HTTPRequest].Path.decode()
            #ip = pkt[scapy.IP]
            print(pkt.src)
            method = pkt[HTTPRequest].Method.decode()
            print(f"{'s'} requested {url} -> {method}")

            if pkt.haslayer(Raw) and method=="POST":
                print(f"Raw: {pkt[Raw].load}")

        

