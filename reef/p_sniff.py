import scapy.all as scapy
from scapy.layers.http import HTTPRequest
from scapy.layers.inet import IP
from scapy.packet import Raw

class Sniffer:
    def __init__(self):
        pass

    def sniff_packets(self):
        scapy.sniff(filter='tcp port 80', prn=self.process, store=True)

    def process(self, pkt: scapy.Packet):
        if pkt.haslayer(HTTPRequest):
            url = pkt[HTTPRequest].Host.decode()+pkt[HTTPRequest].Path.decode()
            #ip = pkt[scapy.IP]
            print(pkt.src)
            method = pkt[HTTPRequest].Method.decode()
            print(f"{'s'} requested {url} -> {method}")

            if pkt.haslayer(Raw) and method=="POST":
                print(f"Raw: {pkt[Raw].load}")

        

